document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatContainer = document.getElementById('chat-container');

    chatForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const userInput = chatInput.value.trim();
        if (userInput) {
            // Display user input in chat
            const userMessage = document.createElement('div');
            userMessage.classList.add('user-message');
            userMessage.innerText = userInput;
            chatContainer.appendChild(userMessage);

            // Send user input to the backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput }),
            });

            const data = await response.json();
            const botMessage = document.createElement('div');
            botMessage.classList.add('bot-message');
            botMessage.innerText = data.response;
            chatContainer.appendChild(botMessage);

            chatInput.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });
});
