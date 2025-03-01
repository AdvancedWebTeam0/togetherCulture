document.addEventListener('DOMContentLoaded', function() {
    // Handle saving tag when the button is clicked
    const saveButton = document.getElementById('save-new-tag-btn');
    const tagInput = document.getElementById('new-tag-name');
    if (saveButton && tagInput) {
        saveButton.addEventListener('click', function() {
            const tagName = tagInput.value;
            if (tagName) {
                // Send a POST request to save the tag
                fetch('./save-tag/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({ tag_name: tagName })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Tag saved!');
                        tagInput.value = '';  // Clear the input after saving
                    } else {
                        console.log('Error saving tag');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Handle saving label when the button is clicked
    const saveButton = document.getElementById('save-new-label-btn');
    const labelInput = document.getElementById('new-label-name');
    if (saveButton && labelInput) {
        saveButton.addEventListener('click', function() {
            const labelName = labelInput.value;
            if (labelName) {
                // Send a POST request to save the label
                fetch('./save-label/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({ label_name: labelName })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('label saved!');
                        labelInput.value = '';  // Clear the input after saving
                    } else {
                        console.log('Error saving label');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Get references to the elements
    var addTagButton = document.getElementById('add-tag-btn');
    var newTagForm = document.getElementById('new-tag-form');
  
    // Check if the button and form exist before attaching event listeners
    if (addTagButton && newTagForm) {
        // Add an event listener to the "+" button
        addTagButton.addEventListener('click', function() {
            // Toggle the visibility of the tag creation form
            if (newTagForm.style.display === 'none' || newTagForm.style.display === '') {
                newTagForm.style.display = 'block';  // Show the form
            } else {
                newTagForm.style.display = 'none';  // Hide the form
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Get references to the elements
    var addLabelButton = document.getElementById('add-label-btn');
    var newLabelForm = document.getElementById('new-label-form');
  
    // Check if the button and form exist before attaching event listeners
    if (addLabelButton && newLabelForm) {
        // Add an event listener to the "+" button
        addLabelButton.addEventListener('click', function() {
            // Toggle the visibility of the tag creation form
            if (newLabelForm.style.display === 'none' || newLabelForm.style.display === '') {
                newLabelForm.style.display = 'block';  // Show the form
            } else {
                newLabelForm.style.display = 'none';  // Hide the form
            }
        });
    }
});