function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function handleInitialInterests(event){
    event.preventDefault();
    var checkboxes = document.getElementsByName("interest_checkbox");
    console.log(checkboxes);  
    var checkboxesChecked = [];

    for (let i = 0; i < checkboxes.length; i++) {
        const curr_checkbox = checkboxes[i];
        if(curr_checkbox.checked){
            checkboxesChecked.push({
                id: curr_checkbox.value,
                value: curr_checkbox.checked
            });
        }
    }
    console.log(checkboxesChecked);  

    const url = `../saveInitialInterests/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ interests : checkboxesChecked })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
}

function openPopup(){
    var popup_page = window.open("get_interests.html", "", "width=700,height=500");
}
