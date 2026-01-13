
document.addEventListener("DOMContentLoaded", function () {
    checkFlaskRunning().then(isRunning => {
        if (isRunning) {
            fetchUsers(); // Fetch users from backend
        } else {
            loadDummyUsers(); // Load dummy data
        }
    });

    document.getElementById('add-user-form').addEventListener('submit', function (e) {
        e.preventDefault();
        addUser(); // Handle new user submission
    });

    document.querySelector('.btn-filter').addEventListener('click', applyFilters);
});

async function checkFlaskRunning() {
    try {
        const res = await fetch('/flask-check');
        return res.ok;
    } catch (e) {
        return false;
    }
}

function applyFilters() {
    fetchUsers(); // Re-fetch users based on selected filters
}

function fetchUsers() {
    const name = document.getElementById('filter-name')?.value.trim() || '';
    const age = document.getElementById('filter-age')?.value || '';
    const gender = document.getElementById('filter-gender')?.value || '';
    const interests = document.getElementById('filter-interests')?.value || '';

    let query = `?name=${encodeURIComponent(name)}&age=${encodeURIComponent(age)}&gender=${encodeURIComponent(gender)}&interests=${encodeURIComponent(interests)}`;

    fetch('/api/admin/users' + query)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                displayUsers(data);
            } else {
                document.querySelector('#users-table tbody').innerHTML = "<tr><td colspan='8'>No users found</td></tr>";
            }
        })
        .catch(error => {
            console.error('Error fetching users:', error);
            document.querySelector('#users-table tbody').innerHTML = "<tr><td colspan='8'>Error fetching users</td></tr>";
        });
}

function displayUsers(users) {
    const tableBody = document.querySelector('#users-table tbody');
    tableBody.innerHTML = '';

    if (!users || users.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='8'>No users found</td></tr>";
        return;
    }

    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.User_ID}</td>
            <td>${user.Name}</td>
            <td>${user.Nationality}</td>
            <td>${user.Age}</td>
            <td>${user.Gender}</td>
            <td>${user.Interests}</td>
            <td>${user.Join_Date}</td>
            <td><button onclick="deleteUser('${user.User_ID}')">Delete</button></td>
        `;
        tableBody.appendChild(row);
    });
}

function addUser() {
    const userData = {
        name: document.getElementById('new-name').value.trim(),
        nationality: document.getElementById('new-nationality').value.trim(),
        email: document.getElementById('new-email').value.trim(),
        password: document.getElementById('new-password').value.trim(),
        phone: document.getElementById('new-phone').value.trim(),
        age: document.getElementById('new-age').value.trim(),
        gender: document.getElementById('new-gender').value.trim(),
        interests: document.getElementById('new-interests').value.trim()
    };

    fetch('/api/admin/add_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchUsers();
    })
    .catch(error => {
        console.error('Error adding user:', error);
        alert('Error adding user. Please try again.');
    });
}

function deleteUser(userId) {
    fetch(`/api/admin/delete_user?user_id=${userId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchUsers();
    })
    .catch(error => {
        console.error('Error deleting user:', error);
        alert('Error deleting user. Please try again.');
    });
}

function loadDummyUsers() {
    const dummyUsers = [
        {
            User_ID: 'U001',
            Name: 'Alice',
            Nationality: 'India',
            Age: 25,
            Gender: 'Female',
            Interests: 'Travel, Art',
            Join_Date: '2024-04-01'
        },
        {
            User_ID: 'U002',
            Name: 'Bob',
            Nationality: 'USA',
            Age: 30,
            Gender: 'Male',
            Interests: 'Music, Hiking',
            Join_Date: '2024-03-20'
        }
    ];
    displayUsers(dummyUsers);
}
