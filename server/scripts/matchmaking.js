// Notify server when leaving the matchmaking page
window.addEventListener('beforeunload', function () {
    setTimeout(function () {
        fetch('/leave_matchmaking', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }, 2000); // Delay of 2 seconds (2000 milliseconds)
});


document.addEventListener('DOMContentLoaded', () => {
    function updateConnectedUsers() {
        fetch('/connected_users')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('connected_users_count');
                if (element) {
                    element.textContent = `Connected users: ${data.connected_users}/3`;
                }

                // Redirect to matchmaking_done if users connected >= 1
                if (data.connected_users >= 1) {
                    window.location.href = '/matchmaking_done';
                }
            })
            .catch(console.error);
    }

    // Poll every 1 second
    setInterval(updateConnectedUsers, 1000);
});

