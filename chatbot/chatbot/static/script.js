function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    if (!userInput.trim()) return;

    // Display user message
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    // Clear input
    document.getElementById("user-input").value = "";

    // Send request to server
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        chatBox.innerHTML += `<p><strong>BOT:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto scroll to bottom
    })
    .catch(error => console.error("Error:", error));
}
