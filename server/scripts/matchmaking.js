// Notify server when leaving the matchmaking page
window.addEventListener('beforeunload', function () {
    fetch('/leave_matchmaking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    function updateConnectedUsers() {
        fetch('/connected_users')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('connected_users_count');
                if (element) {
                    element.textContent = `Connected users: ${data.connected_users}`;
                }
            })
            .catch(console.error);
    }

    // Poll every x seconds
    setInterval(updateConnectedUsers, 100);
});
