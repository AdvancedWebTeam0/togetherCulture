function toggleSubMenu() {
    var submenu = document.getElementById("subitemNav");
    var triangle = document.getElementById("triangleIcon");
    if (submenu.style.display === "flex") {
        submenu.style.display = "none";
        triangle.classList.remove("rotate");
    } else {
        submenu.style.display = "flex";
        triangle.classList.add("rotate");
    }
}

// static/js/dashboard.js

document.addEventListener("DOMContentLoaded", function() {
    // Polling for cards with dynamic card IDs (assuming they follow a similar structure)
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        const cardId = card.getAttribute('id').split('-')[1]; // Extracts card ID (e.g., '1' from 'card-1')

        setInterval(function() {
            fetch(`./update-card/${cardId}/`)  // Dynamic URL based on card ID
                .then(response => response.json())
                .then(data => {
                    const cardValueElement = card.querySelector('.card-body .card-value');
                    if (cardValueElement && data.new_value) {
                        cardValueElement.textContent = data.new_value;  // Update the card value
                    }
                })
                .catch(error => console.error(`Error updating card ${cardId}:`, error));
        }, 10000);  // Poll every 60 seconds for each card
    });
});
