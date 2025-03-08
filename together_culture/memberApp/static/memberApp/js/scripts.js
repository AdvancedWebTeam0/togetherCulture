
function bookModule(moduleId) {
    const url = './book/' + moduleId + '/';  // URL to send AJAX request
    const csrftoken = document.querySelector('[name="csrf-token"]').content;  // Get CSRF token from meta tag

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // Include CSRF token in request headers
        },
        body: JSON.stringify({ 'moduleId': moduleId })
    })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById('message' + moduleId);
            if (data.status === 'success') {
                messageElement.innerText = data.message;
                document.getElementById('bookButton' + moduleId).style.display = 'none'; // Hide button after booking
            } else {
                messageElement.innerText = data.message; // Show error message if booking fails
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
