document.addEventListener('DOMContentLoaded', () => {
    function updateConnectedUsers() {
        // Fetch the connected users count
        fetch('/connected_users')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('connected_users_count');
                if (element) {
                    element.textContent = `Connected users: ${data.connected_users}/3`;
                }

                // Check if the connected users are 2 or more
                if (data.connected_users >= 3) {
                    checkIfReadyToMatch();
                }
            })
            .catch(console.error);
    }

    function checkIfReadyToMatch() {
        console.log('Checking if ready to match...');
        // Fetch if users are ready to match
        fetch('/ready_to_match')
            .then(response => response.json())
            .then(data => {
                if (data.ready) {
                    console.log('Ready to match!');
                    // If ready, redirect to matchmaking done
                    window.location.href = '/matchmaking_done';
                }
            })
            .catch(console.error);
    }

    // Poll every 1 second to update the connected users count
    setInterval(updateConnectedUsers, 1000);
});
