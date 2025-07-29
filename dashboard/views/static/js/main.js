// Real-time update (opsional)
document.addEventListener('DOMContentLoaded', function() {
    setInterval(() => {
        fetch('/api/auctions')
            .then(response => response.json())
            .then(data => {
                // Implement update logic here
                console.log('Received update', data);
            })
            .catch(error => console.error('Update error:', error));
    }, 10000); // Update setiap 10 detik
});