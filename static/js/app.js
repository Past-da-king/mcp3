
document.addEventListener('DOMContentLoaded', () => { // Ensure DOM is loaded before accessing elements

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messagesDiv = document.getElementById('messages');
    let websocket;

    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        // Ensure this uses the host and port your FastAPI backend is running on.
        // If your FastAPI runs on 8001, window.location.host will be '127.0.0.1:8001' or 'localhost:8001'
        const wsUrl = `${protocol}//${window.location.host}/ws/chat`;
        
        addMessageToDisplay('status', `Attempting to connect to ${wsUrl}...`);
        console.log(`Attempting to connect to WebSocket at ${wsUrl}`);
        websocket = new WebSocket(wsUrl);

        websocket.onopen = () => {
            addMessageToDisplay('status', 'Connected to Calculon\'s relay.');
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
                    addMessageToDisplay('thought', `${data.content}`); // Removed "Calculon's thought:" prefix here, as it's in the styling
                    startNewAiMessageIfNeeded(); 
                    break;
                case 'tool_call':
                    addMessageToDisplay('tool_call', `Wants to use tool: ${data.content.name} with args: ${JSON.stringify(data.content.args)}`);
                    startNewAiMessageIfNeeded();
                    break;
                case 'tool_response':
                    addMessageToDisplay('tool_call', `Tool ${data.content.name} responded.`); // Style as tool_call
                    startNewAiMessageIfNeeded();
                    break;
                case 'status':
                    addMessageToDisplay('status', data.content);
                    break;
                case 'mcp_tools':
                    // This is just an example of handling a custom message type
                    // addMessageToDisplay('status', `Available MCP Tools: ${data.content.join(', ')}`);
                    console.log(`Available MCP Tools from server: ${data.content.join(', ')}`);
                    break;
                case 'stream_end':
                    addMessageToDisplay('status', data.content);
                    currentAiMessageElement = null; // Reset for next AI message
                    messageInput.focus();
                    break;
                case 'error':
                    addMessageToDisplay('error', `Error from server: ${data.content}`, true);
                    currentAiMessageElement = null;
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

    function addMessageToDisplay(type, text, isError = false) {
        currentAiMessageElement = null; // New message, so not appending to previous AI
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
                messageElement.classList.add('user-message'); // Tailwind: bg-blue-500 text-white
                messageElement.textContent = text;
                break;
            case 'thought':
                messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('thought-message'); // Tailwind: bg-yellow-100 text-yellow-800 border-yellow-400
                iconHtml = '<i class="fas fa-brain fa-fw mr-2"></i>';
                senderText = 'Calculon\'s Internal Monologue';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                break;
            case 'tool_call':
                 messageWrapper.classList.add('flex', 'justify-start');
                messageElement.classList.add('tool-call-message'); // Tailwind: bg-indigo-100 text-indigo-800 border-indigo-400
                iconHtml = '<i class="fas fa-wrench fa-fw mr-2"></i>';
                senderText = 'Tool Interaction';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                break;
            case 'status':
                messageWrapper.classList.add('status-wrapper'); // No flex by default for status
                messageElement.classList.add('status-message'); // Tailwind: text-gray-500 italic text-center text-sm
                messageElement.textContent = text;
                break;
            case 'error':
                messageWrapper.classList.add('flex', 'justify-start'); // Or center, depending on desired error appearance
                messageElement.classList.add('error-message'); // Tailwind: bg-red-100 text-red-700 border-red-400
                iconHtml = '<i class="fas fa-exclamation-triangle fa-fw mr-2"></i>';
                senderText = 'System Error';
                messageElement.innerHTML = `<span class="sender block font-semibold mb-1">${iconHtml}${senderText}</span>${escapeHtmlAndPreserveFormatting(text)}`;
                break;
            // AI text chunks are handled by startNewAiMessageIfNeeded and appendAiMessageChunk
        }
        
        if (type !== 'text_chunk') { // text_chunk is handled differently
            messageWrapper.appendChild(messageElement);
            messagesDiv.appendChild(messageWrapper);
        }
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    function startNewAiMessageIfNeeded() {
        // This function ensures that thoughts or tool calls create a new bubble
        // before any subsequent AI text starts appending to a new text bubble.
        if (currentAiMessageElement) { // If there was an AI text bubble being appended to
            currentAiMessageElement = null; // Force a new one for the next text_chunk
            currentAiTextContentDiv = null;
        }
    }

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

            currentAiTextContentDiv = document.createElement('div');
            currentAiTextContentDiv.classList.add('ai-text-content');
            currentAiMessageElement.appendChild(currentAiTextContentDiv);
            
            messageWrapper.appendChild(currentAiMessageElement);
            messagesDiv.appendChild(messageWrapper);
        }
    }

    function appendAiMessageChunk(textChunk) {
        ensureAiMessageBubbleExists(); // Make sure we have an AI message bubble
        if (currentAiTextContentDiv) {
            // Append formatted text. `escapeHtmlAndPreserveFormatting` handles <br> for newlines.
            currentAiTextContentDiv.innerHTML += escapeHtmlAndPreserveFormatting(textChunk);
        }
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
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

    // Initialize: Disable inputs and attempt to connect
    if (messageInput) messageInput.disabled = true;
    if (sendButton) sendButton.disabled = true;
    
    connectWebSocket();

}); // End of DOMContentLoaded