document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('event-search-form').addEventListener('submit', function (e) {
        e.preventDefault(); // Prevent regular form submission

        // Get selected tags and labels
        let selectedTags = [];
        let selectedLabels = [];

        document.querySelectorAll('#tags option:checked').forEach(function (option) {
            selectedTags.push(option.value);  // Push selected tag into the array
        });

        document.querySelectorAll('#labels option:checked').forEach(function (option) {
            selectedLabels.push(option.value);  // Push selected label into the array
        });

        // Build the query string with selected tags and labels
        let queryParams = new URLSearchParams();

        // Check if tags have been selected and append them
        if (selectedTags.length > 0) {
            queryParams.append('tags', selectedTags.join(','));  // Join tags with commas
        }

        // Check if labels have been selected and append them
        if (selectedLabels.length > 0) {
            queryParams.append('labels', selectedLabels.join(','));  // Join labels with commas
        }

        // Send AJAX request
        fetch("/admin/event-search/?" + queryParams.toString(), {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  // Ensure this is sent
                'Content-Type': 'application/json'  // For sending JSON data (optional)
            }
        })
            .then(response => response.json())
            .then(data => {
                let eventResults = document.getElementById('event-results');
                eventResults.innerHTML = '';  // Clear previous results

                if (data.error) {
                    eventResults.innerHTML = `<p>${data.error}</p>`;  // Display error message if no events found
                } else {
                    data.events.forEach(event => {
                        let eventElement = document.createElement('div');
                        eventElement.innerHTML = `
            <h3>Event Name; ${event.title}</h3>
            <p>Event Description: ${event.description}</p>
            <p>Tags: ${event.tags.join(', ')}</p>
            <p>Labels: ${event.labels.join(', ')}</p>
        `;
                        eventResults.appendChild(eventElement);
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});