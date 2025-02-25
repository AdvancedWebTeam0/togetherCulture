function handleInitialInterests(event){
    print("Here!!!");
    event.preventDefault();
    var checkboxes = document.getElementsByName("interest_checkbox");
    var checkboxesChecked = [];

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i]);
        }
    }

    const url = `../saveInitialInterests`;
    /*const url = `../saveInitialInterests/?interests=${encodeURIComponent(checkboxesChecked)}`;*/

    fetch(url, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            if (response.redirected) {
                window.location.href = response.url;
                return null;
            }
            return response.text();
        }
        return response.json().then(errorData => {
            throw new Error(errorData.message);
        });
    })
    .then(data => {
        if (data) {
            document.open();
            document.write(data);
            document.close();
        }
    })
    .catch(error => {
        alert(`Unexpected error: ${error.message}`);
    });


    /*event.preventDefault();
    var checkboxes = document.getElementsByName("interest_checkbox");
    var checkboxesChecked = [];

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxesChecked.push(checkboxes[i]);
        }
    }

    const url = `../saveInitialInterests/?interests=${encodeURIComponent(checkboxesChecked)}`;

    fetch(url, {
        method: 'POST'
    })
    .catch(error => {
        alert(`Unexpected error: ${error.message}`);
    });

    /*if(checkboxesChecked.length > 0){
        const requestObject = new XMLHttpRequest()
        requestObject.open("GET", "/saveInitialInterests/");
        requestObject.send(checkboxesChecked);
    }
    else{
        print("NULL")
    }*/
}

function openPopup(){
    var popup_page = window.open("get_interests.html", "", "width=700,height=500");
}
