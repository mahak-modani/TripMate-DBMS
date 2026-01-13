document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    let formData = {
        email: email,
        password: password
    };

    fetch('/api/user/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show the message from the backend
        
        if (data.redirect) {
            window.location.href = data.redirect;  // Redirect to login page if signup is successful
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
});
