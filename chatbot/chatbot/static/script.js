function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto scroll to bottom
}

function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    // Display user message
    appendMessage("You", userInput);

    // Clear input
    document.getElementById("user-input").value = "";

    // Show loading indicator
    appendMessage("BOT", "Typing...");

    // Send request to server
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        // Remove loading indicator and display bot response
        const chatBox = document.getElementById("chat-box");
        chatBox.lastChild.remove(); // Remove the "Typing..." message
        appendMessage("BOT", data.response);
    })
    .catch(error => {
        console.error("Error:", error);
        // Display error message
        appendMessage("BOT", "Sorry, there was an error processing your request.");
    });
}
