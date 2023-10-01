document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#post-form').addEventListener('submit', submitPost);
    document.querySelectorAll('.edit-link').forEach(link => {
        link.addEventListener('click', editPost);
    });
    document.querySelectorAll('.save-button').forEach(button => {
        button.addEventListener('click', savePost);
    });
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

function editPost(event) {
    event.preventDefault();
    
    // Get the post ID from the data attribute
    const postId = event.currentTarget.getAttribute('data-post-id');

    // Hide the "Edit" link
    event.currentTarget.style.display = 'none';

    // Hide the current content
    const contentElement = document.querySelector(`#content-${postId}`);
    const textarea = document.querySelector(`#edit-textarea-${postId}`);
    const saveButton = document.querySelector(`#save-button-${postId}`);
    
    contentElement.style.display = 'none';
    textarea.style.display = 'block';
    saveButton.style.display = 'block';
}


function savePost(event) {
    const postId = event.currentTarget.getAttribute('data-post-id');
    const editedContent = document.querySelector(`#edit-textarea-${postId}`).value;
    const data = {
        postId: postId,
        editedContent: editedContent
    }
    fetch(`/edit_post`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(result => {
        const contentElement = document.querySelector(`#content-${postId}`);
        const contentWithLineBreaks = result.post_content.replace(/\n/g, '<br>');
        
        contentElement.innerHTML = contentWithLineBreaks;
        contentElement.style.display = 'block';
        
        document.querySelector(`#edit-textarea-${postId}`).style.display = 'none';
        document.querySelector(`#save-button-${postId}`).style.display = 'none';
        document.querySelector(`#edit-link-${postId}`).style.display = 'block';
    }); 
}