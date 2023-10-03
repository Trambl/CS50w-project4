document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.querySelector('#post-form');
    if (postForm) {
        postForm.addEventListener('submit', submitPost);
    }
    
    document.querySelectorAll('.edit-link').forEach(link => {
        link.addEventListener('click', editPost);
    });
    document.querySelectorAll('.save-button').forEach(button => {
        button.addEventListener('click', savePost);
    });
    document.querySelectorAll('.red-heart').forEach(button => {
        button.addEventListener('click', likePost);
    })
    
    const followButton = document.querySelector('.follow-button');
    if (followButton) {
        followButton.addEventListener('click', followUser);
    }
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
    .then(response => {
        if (response.status === 401) {
            // Unauthorized user, redirect to the login page
            window.location.href = '/login'; // Update the URL to your login page
        }
        if (response.status === 200) {
            return response.json();
        } else {
            // Handle other response statuses here if needed
            console.error('Failed to submit post');
        }
    })
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

function likePost(event) {
    const postId = event.currentTarget.getAttribute('data-post-id');
    const data = {
        postId: postId
    }
    fetch(`/like_post`, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (response.status === 401) {
            // Unauthorized user, redirect to the login page
            window.location.href = '/login'; // Update the URL to your login page
        }
        if (response.status === 200) {
            return response.json();
        } else {
            // Handle other response statuses here if needed
            console.error('Failed to like the post');
        }
    })
    .then(result => {
        console.log(result)
        const icon = document.querySelector(`#like-icon-${postId}`);
        
        if (result.liked) {
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill');
        }
        else {
            icon.classList.remove('bi-heart-fill');
            icon.classList.add('bi-heart');
        }
        document.querySelector(`#num-likes-${postId}`).innerHTML = result.num_likes;
    })
}

function followUser(event) {
    const followingId = event.currentTarget.getAttribute('data-following-id')
    const followingUsername = event.currentTarget.getAttribute('data-following-username')
    const data = {
        'followingId': followingId,
    }
    fetch(`/profile/${followingUsername}`, {
        method: 'POST',
        data: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(result => {
        const followButton = document.querySelector('.follow-button');
        if (result.followed) {
            followButton.innerHTML = 'Unfollow';
        }
        else {
            followButton.innerHTML = 'Follow';
        }
        const numFollowers = document.querySelector('#num-followers')
        const numFollowings = document.querySelector('#num-followings')
        numFollowers.innerHTML = `Followers: ${result.num_followers}`;
        numFollowings.innerHTML = `Followings: ${result.num_followings}`;
    })
}