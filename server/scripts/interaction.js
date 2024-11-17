const socket = io();  // Initialize SocketIO connection

document.addEventListener("DOMContentLoaded", function () {
    let countdownValue = 90;  // Start at 1 minute (90 seconds)
    const countdownElement = document.getElementById("countdown");
    const chatBox = document.getElementById("chatBox");
    const chatInput = document.getElementById("chatInput");

    // Countdown timer logic
    const countdownInterval = setInterval(function () {
        countdownValue--;
        countdownElement.textContent = countdownValue;

        if (countdownValue <= 0) {
            clearInterval(countdownInterval);
        }
    }, 1000);

    // Handle Chat Input
    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            const message = chatInput.value.trim();
            if (message) {
                // Emit message to server
                console.log("Sending message: " + message);  // Log the sent message
                socket.emit('send_message', { message: message });

                // Display message locally for user
                const userMessage = document.createElement("div");
                userMessage.classList.add("chat-message", "user");
                userMessage.textContent = message;
                chatBox.appendChild(userMessage);

                // Scroll to the bottom of the chat
                chatBox.scrollTop = chatBox.scrollHeight;

                // Clear input
                chatInput.value = "";
            }
        }
    });

    // Listen for incoming messages
    // Listen for the 'receive_message' event
    socket.on('receive_message', function (data) {  // Listen for 'receive_message' event
        console.log(`Received message from user ${data.user_id}: ${data.message}`);  // Log received message
    
        // Display the message in the chat
        const chatBox = document.getElementById('chatBox');
        const chatMessage = document.createElement('div');
        
        chatMessage.classList.add('chat-message', 'other');  // 'other' class for the received message
        chatMessage.textContent = data.message;
    
        chatBox.appendChild(chatMessage);
        chatBox.scrollTop = chatBox.scrollHeight;  // Scroll to the bottom
    });

    document.getElementById('rejectButton').addEventListener('click', function() {
        // Emit the 'reject_match' event without needing user_id from JavaScript
        socket.emit('reject_match'); // Send the event to the server to handle rejection
    });

    socket.on('redirect_to_why', function() {
        // Redirect to the 'why' page
        console.log("Redirecting to 'why' page...");
        window.location.href = '/why';
    });

    socket.on('redirect_to_congratulations', function () {
        // Redirect to the 'congratulations' page
        console.log("Redirecting to 'congratulations' page...");
        window.location.href = '/congratulations';
    });

    document.getElementById("acceptButton").addEventListener("click", function () {
        socket.emit("accept_match");  // Emit the 'accept_match' event
    });
});
