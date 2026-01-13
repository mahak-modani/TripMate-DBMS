document.addEventListener("DOMContentLoaded", function () {
    // ✅ Fetch user data from the backend
    fetch('/api/user/profile_settings', { headers: { 'Accept': 'application/json' } })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = "/login";  // 🔁 Redirect if not logged in
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(user => {
            // ✅ Fill form fields with retrieved user data
            document.getElementById('name').value = user.Name || "";
            document.getElementById('email').value = user.Email || "";
            document.getElementById('phone').value = user.Phone_Number || "";
            document.getElementById('age').value = user.Age || "";
            document.getElementById('gender').value = user.Gender || "";
            document.getElementById('nationality').value = user.Nationality || "";
            document.getElementById('interests').value = user.Interests || "";
        })
        .catch(error => {
            console.warn("Using default values. Reason:", error);
        });

    // ✅ Handle form submission
    document.getElementById('profile-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone_number: document.getElementById('phone').value,
            age: document.getElementById('age').value,
            gender: document.getElementById('gender').value,
            nationality: document.getElementById('nationality').value,
            interests: document.getElementById('interests').value
        };

        // ✅ Send updated user data to backend
        fetch('/api/user/profile_settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "Updated!");
            if (data.success) {
                window.location.reload();  // 🔁 Reload page if update was successful
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred. Please try again.");
        });
    });
});
