
function sendMessage() {
    const chatWindow = document.getElementById('chatWindow');
    const inputField = document.getElementById('inputField');
    const userMessage = inputField.value.trim();

    if (userMessage.length > 0) {
        // Display user's message
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'message user-message';
        userMessageElement.textContent = userMessage;
        chatWindow.appendChild(userMessageElement);

        // Clear and focus the input field
        inputField.value = '';
        inputField.focus();

        // Simulate bot response
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message bot-message';
        botMessageElement.textContent = 'Processing your request...';
        chatWindow.appendChild(botMessageElement);

        // Auto-scroll to the latest message
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Send user message to the server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Update the bot message with the response
            botMessageElement.textContent = data.response;
            chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the latest message
        })
        .catch(error => {
            console.error('Error:', error);
            botMessageElement.textContent = 'Sorry, I couldn\'t process your request.';
            chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the latest message
        });
    }
function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}


}