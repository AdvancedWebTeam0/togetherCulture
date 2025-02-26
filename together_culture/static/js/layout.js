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

document.addEventListener("DOMContentLoaded", function() {
    // Loop through each card and set up its individual interval
    document.querySelectorAll('.card').forEach(function(card) {
        const cardId = card.id.split('-')[1]; // Extract card ID from 'card-1', 'card-2', etc.
        const interval = card.getAttribute('data-interval');  // Get the interval for this card

        // Set polling for this card with its own interval
        setInterval(function() {
            fetch(`./update-card/${cardId}/`)
                .then(response => response.json())
                .then(data => {
                    const cardValueElement = card.querySelector('.card-body .card-value');
                    if (cardValueElement && data.new_value) {
                        cardValueElement.textContent = data.new_value;  // Update the card value with new data
                    }
                })
                .catch(error => console.error(`Error updating card ${cardId}:`, error));
        }, parseInt(interval));  // Use the unique interval for this card
    });
});
