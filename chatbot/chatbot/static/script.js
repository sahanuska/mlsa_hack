function appendMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageElement = document.createElement("p");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}


function sendMessage() {
    const userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;
    appendMessage("You", userInput);
    document.getElementById("user-input").value = "";

    appendMessage("BOT", "Typing...");

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
        const chatBox = document.getElementById("chat-box");
        chatBox.lastChild.remove(); 
        appendMessage("BOT", data.response);
    })
    .catch(error => {
        console.error("Error:", error);
        appendMessage("BOT", "Sorry, there was an error processing your request.");
    });
}
