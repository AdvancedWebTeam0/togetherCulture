
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

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".use-benefit-btn").forEach(button => {
        button.addEventListener("click", function () {
            let benefitId = this.getAttribute("data-id");
            const url = document.getElementById('benefits').getAttribute('data-url');

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({})
            })
                .then(response => response.json())
                .then(data => {
                    let messageContainer = document.querySelector(`.benefit-message[data-id='${benefitId}']`);
                    messageContainer.style.display = "block"; // Show message
                    messageContainer.textContent = data.message;

                    if (data.success) {
                        messageContainer.style.color = "green"; // Success message color
                        document.querySelector(`.benefit-card[data-id='${benefitId}'] .remaining`).textContent = data.remaining;
                    } else {
                        messageContainer.style.color = "red"; // Error message color
                    }
                })
                .catch(error => console.error("Fetch Error:", error));
        });
    });
});
