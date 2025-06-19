
document.addEventListener('DOMContentLoaded', () => { // Ensure DOM is loaded before accessing elements

    const CHAT_HISTORY_KEY = 'calculonChatHistory';

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const clearChatButton = document.getElementById('clearChatButton');
    const messagesDiv = document.getElementById('messages');
    let websocket;

    // --- Toast Notification Function ---
    function showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.textContent = message;
        let bgColorClass = 'bg-blue-500'; // Default to info
        if (type === 'success') {
            bgColorClass = 'bg-green-500';
        } else if (type === 'error') {
            bgColorClass = 'bg-red-500';
        }

        toast.className = `fixed top-5 right-5 p-4 rounded-lg shadow-lg text-white text-sm z-50 transition-opacity duration-300 ease-in-out ${bgColorClass}`;

        document.body.appendChild(toast);

        // Trigger fade in after append (opacity is initially 0 via CSS or could be set here)
        // For simplicity, we'll make it appear immediately then fade out.
        // If we wanted a fade-in, we'd set opacity to 0 initially, then to 1 in a setTimeout(..., 10)

        setTimeout(() => {
            toast.style.opacity = '0';
        }, duration - 300); // Start fade out 300ms before removal

        setTimeout(() => {
            toast.remove();
        }, duration);
    }


    // --- Chat History Functions ---
    function saveMessageToHistory(messageObject) {
        try {
            const history = JSON.parse(localStorage.getItem(CHAT_HISTORY_KEY)) || [];
            history.push(messageObject);
            localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(history));
        } catch (e) {
            console.error("Error saving message to localStorage:", e);
        }
    }

    function loadChatHistory() {
        try {
            const history = JSON.parse(localStorage.getItem(CHAT_HISTORY_KEY));
            if (history && Array.isArray(history)) {
                messagesDiv.innerHTML = ''; // Clear any existing messages (e.g., initial status)
                history.forEach(msg => {
                    switch (msg.type) {
                        case 'user':
                            // Call original addMessageToDisplay but prevent re-saving
                            addMessageToDisplay(msg.type, msg.content, false, true);
                            break;
                        case 'ai':
                            ensureAiMessageBubbleExists();
                            if (currentAiMessageElement) { // Should exist now
                                const senderSpan = currentAiMessageElement.querySelector('.sender');
                                if (senderSpan) senderSpan.innerHTML = `<i class="fas fa-robot fa-fw mr-2"></i>${msg.sender || 'Calculon'}`;
                                if (currentAiTextContentDiv) currentAiTextContentDiv.innerHTML = msg.htmlContent;
                            }
                            startNewAiMessageIfNeeded(); // Finalize this AI message bubble
                            break;
                        case 'thought':
                        case 'tool_call':
                        case 'error':
                             // Call original addMessageToDisplay but prevent re-saving
                            addMessageToDisplay(msg.type, msg.content, msg.type === 'error', true);
                            break;
                        case 'status':
                             // Call original addMessageToDisplay but prevent re-saving
                            addMessageToDisplay(msg.type, msg.content, false, true);
                            break;
                        default:
                            console.warn("Unknown message type in history:", msg);
                    }
                });
                // After loading all, ensure the view is scrolled to the bottom
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        } catch (e) {
            console.error("Error loading chat history from localStorage:", e);
            // Optionally, clear corrupted history: localStorage.removeItem(CHAT_HISTORY_KEY);
        }
    }


    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
        
        // Don't add initial connecting message if history will be loaded
        if (!(JSON.parse(localStorage.getItem(CHAT_HISTORY_KEY))?.length > 0)) {
            addMessageToDisplay('status', `Attempting to connect to ${wsUrl}...`);
        }
        console.log(`Attempting to connect to WebSocket at ${wsUrl}`);
        websocket = new WebSocket(wsUrl);

        websocket.onopen = () => {
            // Status message for successful connection, avoiding duplicates if history loaded one.
            if (messagesDiv.lastChild && messagesDiv.lastChild.textContent !== 'Connected to Calculon\'s relay.') {
                 addMessageToDisplay('status', 'Connected to Calculon\'s relay.');
            } else if (!messagesDiv.lastChild) { // If chat was empty
                 addMessageToDisplay('status', 'Connected to Calculon\'s relay.');
            }
            console.log('WebSocket connected');
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus(); // Focus on input field once connected
        };

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("Received from WS:", data); // Log the raw data

            switch (data.type) {
                case 'text_chunk':
                    appendAiMessageChunk(data.content);
                    break;
                case 'thought':
                    // Thoughts are already displayed in their own bubbles, no separate toast needed.
                    addMessageToDisplay('thought', `${data.content}`);
                    startNewAiMessageIfNeeded(); 
                    break;
                case 'tool_call':
                    // Display thought bubble for tool call
                    addMessageToDisplay('tool_call', `Wants to use tool: ${data.content.name} with args: ${JSON.stringify(data.content.args)}`);
                    // Show toast notification
                    showToast(`Calling tool: ${data.content.name}...`, 'info');
                    startNewAiMessageIfNeeded();
                    break;
                case 'tool_response':
                    // Display thought bubble for tool response
                    addMessageToDisplay('tool_call', `Tool ${data.content.name} responded.`);
                    // Show toast notification
                    showToast(`Tool ${data.content.name} completed.`, 'success');
                    startNewAiMessageIfNeeded();
                    break;
                case 'status':
                    addMessageToDisplay('status', data.content);
                    break;
                case 'mcp_tools':
                    console.log(`Available MCP Tools from server: ${data.content.join(', ')}`);
                    break;
                case 'stream_end':
                    // Save any pending AI message before processing the stream_end status
                    if (currentAiMessageElement && currentAiTextContentDiv && currentAiTextContentDiv.innerHTML.trim() !== '') {
                        saveMessageToHistory({ type: 'ai', sender: 'Calculon', htmlContent: currentAiTextContentDiv.innerHTML });
                    }
                    addMessageToDisplay('status', data.content); // This will save the status message
                    currentAiMessageElement = null; // Reset for next AI message
                    currentAiTextContentDiv = null;
                    messageInput.focus();
                    break;
                case 'error':
                    addMessageToDisplay('error', `Error from server: ${data.content}`);
                    currentAiMessageElement = null; // Reset AI state on error
                    currentAiTextContentDiv = null;
                    break;
                default:
                    console.warn('Unknown message type received:', data.type, data);
            }
        };

        websocket.onclose = (event) => {
            let reason = "";
            if (event.code) reason += `Code: ${event.code} `;
            if (event.reason) reason += `Reason: ${event.reason} `;
            if (event.wasClean) reason += `(Clean close) `; else reason += `(Unclean close) `;
            
            addMessageToDisplay('status', `Disconnected. ${reason}Attempting to reconnect...`, true);
            console.log(`WebSocket disconnected. ${reason}Attempting to reconnect...`);
            messageInput.disabled = true;
            sendButton.disabled = true;
            currentAiMessageElement = null;
            setTimeout(connectWebSocket, 3000); // Try to reconnect after 3 seconds
        };

        websocket.onerror = (error) => {
            // This event often fires just before onclose when there's a connection issue
            addMessageToDisplay('error', 'WebSocket connection error. Check console and server logs.', true);
            console.error('WebSocket error:', error);
            // onclose will likely handle disabling inputs and attempting reconnection
        };
    }

    let currentAiMessageElement = null;
    let currentAiTextContentDiv = null;

    // Modified to prevent re-saving when loading from history
    function addMessageToDisplay(type, text, isError = false, isLoadingHistory = false) {
        // Save any pending AI message before adding a new non-chunk message
        if (!isLoadingHistory && currentAiMessageElement && currentAiTextContentDiv && currentAiTextContentDiv.innerHTML.trim() !== '') {
            saveMessageToHistory({ type: 'ai', sender: 'Calculon', htmlContent: currentAiTextContentDiv.innerHTML });
        }
        // For all message types (including AI messages that are now complete), reset current AI tracking
        currentAiMessageElement = null;
        currentAiTextContentDiv = null;

        const messageWrapper = document.createElement('div');
        // Basic wrapper, flex alignment is handled by message type specific classes now if needed
        // messageWrapper.classList.add('message-wrapper', `${type}-wrapper`);

        const messageElement = document.createElement('div');
        // Generic message classes removed, specific styles per type applied below
        
        let iconHtml = '';
        let senderText = ''; // Not used for user messages directly in bubble

        switch (type) {
            case 'user':
                messageWrapper.className = 'flex justify-end'; // Wrapper for alignment
                messageElement.className = 'user-message bg-blue-500 text-white p-3 rounded-lg max-w-xs lg:max-w-md break-words shadow';
                messageElement.textContent = text;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'user', content: text });
                break;
            case 'thought':
                messageWrapper.className = 'flex justify-start'; // Wrapper for alignment
                messageElement.className = 'thought-message bg-yellow-100 border-l-4 border-yellow-400 text-yellow-800 p-3 rounded-r-lg max-w-xs lg:max-w-md text-sm italic break-words shadow';
                iconHtml = '<i class="fas fa-brain fa-fw mr-1"></i>';
                senderText = 'Calculon\'s Internal Monologue';
                messageElement.innerHTML = `<span class="sender block text-xs font-semibold mb-1 text-yellow-700">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'thought', sender: senderText, content: text });
                break;
            case 'tool_call':
                messageWrapper.className = 'flex justify-start'; // Wrapper for alignment
                messageElement.className = 'tool-call-message bg-indigo-100 border-l-4 border-indigo-400 text-indigo-800 p-3 rounded-r-lg max-w-xs lg:max-w-md text-sm break-words shadow';
                iconHtml = '<i class="fas fa-wrench fa-fw mr-1"></i>';
                senderText = 'Tool Interaction';
                messageElement.innerHTML = `<span class="sender block text-xs font-semibold mb-1 text-indigo-700">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'tool_call', sender: senderText, content: text });
                break;
            case 'status':
                messageWrapper.className = 'status-wrapper w-full'; // Wrapper for alignment
                messageElement.className = 'status-message text-gray-500 text-xs italic text-center py-2';
                messageElement.textContent = text;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'status', content: text });
                break;
            case 'error':
                messageWrapper.className = 'flex justify-start'; // Wrapper for alignment
                messageElement.className = 'error-message bg-red-100 border-l-4 border-red-400 text-red-800 p-3 rounded-r-lg max-w-xs lg:max-w-md text-sm break-words shadow';
                iconHtml = '<i class="fas fa-exclamation-triangle fa-fw mr-1"></i>';
                senderText = 'System Error';
                messageElement.innerHTML = `<span class="sender block text-xs font-semibold mb-1 text-red-700">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'error', sender: senderText, content: text });
                break;
        }
        
        // This part remains for display, AI chunks are handled by appendAiMessageChunk
        // AI messages are constructed in ensureAiMessageBubbleExists
        if (type !== 'text_chunk' && type !== 'ai') {
            messageWrapper.appendChild(messageElement);
            messagesDiv.appendChild(messageWrapper);
        }
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function startNewAiMessageIfNeeded() {
        // This function is called when a new non-AI message starts,
        // or when an AI stream ends, to finalize the current AI bubble.
        // The saving of the AI message content should have happened just before this in addMessageToDisplay or stream_end.
        if (currentAiMessageElement) {
            currentAiMessageElement = null;
            currentAiTextContentDiv = null;
        }
    }

    // ensureAiMessageBubbleExists is now primarily for display during streaming or loading history.
    // Saving of the AI message happens when it's complete.
    function ensureAiMessageBubbleExists() {
        if (!currentAiMessageElement) {
            const messageWrapper = document.createElement('div');
            // Wrapper for alignment for AI messages
            messageWrapper.className = 'flex justify-start';

            currentAiMessageElement = document.createElement('div');
            currentAiMessageElement.className = 'ai-message bg-gray-200 text-gray-800 p-3 rounded-lg max-w-xs lg:max-w-md break-words shadow';
            
            const senderSpan = document.createElement('span');
            // Tailwind classes for AI sender
            senderSpan.className = 'sender block text-xs font-semibold mb-1 text-gray-700';
            senderSpan.innerHTML = '<i class="fas fa-robot fa-fw mr-1"></i>Calculon';
            currentAiMessageElement.appendChild(senderSpan);

            currentAiTextContentDiv = document.createElement('div');
            currentAiTextContentDiv.className = 'ai-text-content'; // No specific Tailwind here, inherits from parent
            currentAiMessageElement.appendChild(currentAiTextContentDiv);
            
            messageWrapper.appendChild(currentAiMessageElement);
            messagesDiv.appendChild(messageWrapper);
        }
    }

    function appendAiMessageChunk(textChunk) {
        ensureAiMessageBubbleExists();
        if (currentAiTextContentDiv) {
            const plotIntroPhrases = [
                "here is the plot you requested: ",
                "you can view it at: ",
                "plot generated: " // Adding another common variant
            ];

            let handledAsPlot = false;
            for (const phrase of plotIntroPhrases) {
                const lowerTextChunk = textChunk.toLowerCase();
                const lowerPhrase = phrase.toLowerCase();

                if (lowerTextChunk.startsWith(lowerPhrase)) {
                    const introTextPart = textChunk.substring(0, phrase.length);
                    const urlPart = textChunk.substring(phrase.length).trim();

                    // Validate URL
                    if (urlPart.startsWith('/static/plots/') && urlPart.toLowerCase().endsWith('.png')) {
                        currentAiTextContentDiv.innerHTML += escapeHtmlAndPreserveFormatting(introTextPart);

                        const img = document.createElement('img');
                        img.src = urlPart;
                        img.alt = 'Plot generated by Calculon';
                        // Apply Tailwind classes for styling the image
                        img.className = 'block max-w-full mt-2 mb-2 rounded shadow'; // Added mb-2 for spacing after

                        // Make image clickable to open in new tab
                        const link = document.createElement('a');
                        link.href = urlPart;
                        link.target = '_blank';
                        link.title = 'Click to view full size in new tab';
                        link.appendChild(img);

                        currentAiTextContentDiv.appendChild(link);
                        handledAsPlot = true;
                        break;
                    }
                }
            }

            if (!handledAsPlot) {
                currentAiTextContentDiv.innerHTML += escapeHtmlAndPreserveFormatting(textChunk);
            }
        }
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    // escapeHtml and escapeHtmlAndPreserveFormatting remain unchanged for now
     function escapeHtml(unsafe) {
        if (unsafe === null || typeof unsafe === 'undefined') return '';
        return unsafe
             .toString()
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    function escapeHtmlAndPreserveFormatting(unsafe) {
        let escaped = escapeHtml(unsafe);
        escaped = escaped.replace(/\n/g, '<br>');
        // Basic Markdown-like code block handling (can be improved)
        escaped = escaped.replace(/```([\s\S]*?)```/g, (match, codeContent) => {
            // For code within pre, we need to escape HTML entities that might be in the code itself
            return `<pre class="bg-gray-800 text-white p-2 rounded overflow-x-auto text-sm"><code>${escapeHtml(codeContent.trim())}</code></pre>`;
        });
         // Basic bold and italic
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        escaped = escaped.replace(/\*(.*?)\*/g, '<em>$1</em>');
        return escaped;
    }

    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText && websocket && websocket.readyState === WebSocket.OPEN) {
            addMessageToDisplay('user', messageText); // User message already saved by addMessageToDisplay
            // Add "Calculon is thinking..." message
            addMessageToDisplay('status', 'Calculon is thinking...');

            console.log('Sending message via WebSocket:', messageText);
            websocket.send(JSON.stringify({ message: messageText }));
            messageInput.value = '';
        } else if (!messageText) {
            console.log("Empty message, not sending.");
        } else {
            console.error('Cannot send message. WebSocket state:', websocket ? websocket.readyState : 'WebSocket not initialized', websocket);
            addMessageToDisplay('error', 'Not connected to server. Cannot send message.'); // isError true is default for 'error' type
        }
    }

    // Event Listeners
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    } else {
        console.error("Send button not found!");
    }

    if (messageInput) {
        messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) { // Send on Enter, allow Shift+Enter for newline
                event.preventDefault(); // Prevent default Enter behavior (like form submission)
                sendMessage();
            }
        });
    } else {
        console.error("Message input not found!");
    }

    // Initialize: Disable inputs
    if (messageInput) messageInput.disabled = true;
    if (sendButton) sendButton.disabled = true;

    if (clearChatButton) {
        clearChatButton.addEventListener('click', () => {
            if (messagesDiv) {
                messagesDiv.innerHTML = '';
                localStorage.removeItem(CHAT_HISTORY_KEY);
                addMessageToDisplay('status', 'Chat cleared and history erased.');
                currentAiMessageElement = null;
                currentAiTextContentDiv = null;
                console.log('Chat cleared and history erased by user.');
            } else {
                console.error("Messages div not found for clearing chat!");
            }
        });
    } else {
        console.error("Clear Chat button not found!");
    }
    
    loadChatHistory(); // Load history before connecting WebSocket
    connectWebSocket();

}); // End of DOMContentLoaded