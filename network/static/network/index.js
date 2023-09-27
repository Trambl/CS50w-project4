document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#post-form').addEventListener('submit', submitPost);
});

function getCookie(name) {
    // Function to retrieve the CSRF token from cookies
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function submitPost() {
    // TODO event.preventDefault();  // Add this line to prevent default form submission
    const body = document.querySelector('#newPostText').value;
    if (body.trim().length < 1) {
        return alert("Post should be at least 1 character long");
    }
    
    fetch('/submit_post', {
        method: 'POST',
        body: JSON.stringify({
            body: body
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
        }
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });
}