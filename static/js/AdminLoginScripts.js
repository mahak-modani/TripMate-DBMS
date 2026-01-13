document.getElementById('adminLoginForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!email || !password) {
        alert("Please enter both email and password.");
        return;
    }

    try {
        const response = await fetch('/api/admin/AdminLogin', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const result = await response.json();
        console.log(result);  // Debugging: Log response to console

        if (response.ok) {
            alert(result.message);
            window.location.replace(result.redirect);  // More reliable redirect
        } else {
            document.getElementById('errorMessage').textContent = result.message;
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("Something went wrong. Please try again.");
    }
});
