document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Create an object to hold form data
    let formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    fetch('/api/user/login', {  // Corrected endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Login successful") {
            alert("Login Successful!");
            window.location.href = "/dashboard";  // Redirect to dashboard
        } else {
            alert(data.error || "Invalid Credentials!");
        }
    })
    .catch(error => console.error('Error:', error));
});
