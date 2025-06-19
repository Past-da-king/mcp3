
document.addEventListener('DOMContentLoaded', () => { // Ensure DOM is loaded before accessing elements

    const CHAT_HISTORY_KEY = 'calculonChatHistory';

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const clearChatButton = document.getElementById('clearChatButton');
    const messagesDiv = document.getElementById('messages');
    let websocket;

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
                    addMessageToDisplay('thought', `${data.content}`);
                    startNewAiMessageIfNeeded(); 
                    break;
                case 'tool_call':
                    addMessageToDisplay('tool_call', `Wants to use tool: ${data.content.name} with args: ${JSON.stringify(data.content.args)}`);
                    startNewAiMessageIfNeeded();
                    break;
                case 'tool_response':
                    addMessageToDisplay('tool_call', `Tool ${data.content.name} responded.`);
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
        messageWrapper.classList.add('message-wrapper', `${type}-wrapper`); // For potential outer styling/flex alignment

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${type}-message`);
        
        let iconHtml = '';
        let senderText = '';

        switch (type) {
            case 'user':
                messageWrapper.classList.add('flex', 'justify-end');
                messageElement.classList.add('user-message');
                messageElement.textContent = text;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'user', content: text });
                break;
            case 'thought':
                messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('thought-message');
                iconHtml = '<i class="fas fa-brain fa-fw mr-2"></i>';
                senderText = 'Calculon\'s Internal Monologue';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'thought', sender: senderText, content: text });
                break;
            case 'tool_call':
                 messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('tool-call-message');
                iconHtml = '<i class="fas fa-wrench fa-fw mr-2"></i>';
                senderText = 'Tool Interaction';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'tool_call', sender: senderText, content: text });
                break;
            case 'status':
                messageWrapper.classList.add('status-wrapper');
                messageElement.classList.add('status-message');
                messageElement.textContent = text;
                // Avoid saving repetitive status messages or very initial ones if not desired.
                // For now, saving all status messages.
                if (!isLoadingHistory) saveMessageToHistory({ type: 'status', content: text });
                break;
            case 'error':
                messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('error-message');
                iconHtml = '<i class="fas fa-exclamation-triangle fa-fw mr-2"></i>';
                senderText = 'System Error';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                if (!isLoadingHistory) saveMessageToHistory({ type: 'error', sender: senderText, content: text });
                break;
        }
        
        // This part remains for display, AI chunks are handled by appendAiMessageChunk
        if (type !== 'text_chunk') {
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
            messageWrapper.classList.add('message-wrapper', 'ai-wrapper', 'flex', 'justify-start');

            currentAiMessageElement = document.createElement('div');
            currentAiMessageElement.classList.add('message', 'ai-message'); // Tailwind: bg-gray-200 text-gray-800
            
            const senderSpan = document.createElement('span');
            senderSpan.classList.add('sender', 'block', 'font-semibold', 'mb-1'); // Tailwind classes
            senderSpan.innerHTML = '<i class="fas fa-robot fa-fw mr-2"></i>Calculon';
            currentAiMessageElement.appendChild(senderSpan);

            currentAiTextContentDiv = document.createElement('div'); // This is where AI text goes
            currentAiTextContentDiv.classList.add('ai-text-content');
            currentAiMessageElement.appendChild(currentAiTextContentDiv);
            
            messageWrapper.appendChild(currentAiMessageElement);
            messagesDiv.appendChild(messageWrapper);
        }
    }

    function appendAiMessageChunk(textChunk) {
        ensureAiMessageBubbleExists();
        if (currentAiTextContentDiv) {
            currentAiTextContentDiv.innerHTML += escapeHtmlAndPreserveFormatting(textChunk);
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
            addMessageToDisplay('user', messageText);
            console.log('Sending message via WebSocket:', messageText);
            websocket.send(JSON.stringify({ message: messageText }));
            messageInput.value = '';
            // currentAiMessageElement = null; // Reset for next AI message. Done in addMessageToDisplay.
        } else if (!messageText) {
            console.log("Empty message, not sending.");
        } else {
            console.error('Cannot send message. WebSocket state:', websocket ? websocket.readyState : 'WebSocket not initialized', websocket);
            addMessageToDisplay('error', 'Not connected to server. Cannot send message.', true);
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