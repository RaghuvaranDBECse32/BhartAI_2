document.getElementById("sendBtn").addEventListener("click", async () => {
    const userInput = document.getElementById("userInput").value;
    const chatbox = document.getElementById("chatbox");
    const userMessage = `<div class="message user">${userInput}</div>`;
    chatbox.innerHTML += userMessage;

    const response = await fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_input: userInput })
    });
    const data = await response.json();
    const botMessage = `<div class="message bot">${data.response}</div>`;
    chatbox.innerHTML += botMessage;

    document.getElementById("userInput").value = "";
});
