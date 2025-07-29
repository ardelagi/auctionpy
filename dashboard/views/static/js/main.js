// Real-time update dengan AJAX
function updateAuctions() {
    fetch('/api/auctions')
        .then(response => response.json())
        .then(data => {
            // Proses update tabel
            console.log('Data updated', data);
            // Implementasi update UI sesuai kebutuhan
        });
}

// Update setiap 10 detik
setInterval(updateAuctions, 10000);