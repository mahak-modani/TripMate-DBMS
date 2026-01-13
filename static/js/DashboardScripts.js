document.addEventListener("DOMContentLoaded", function () {
    let userName = localStorage.getItem("user_name");

    if (userName) {
        document.getElementById("welcome-message").innerText = `Welcome, ${userName}!`;
    } else {
        document.getElementById("welcome-message").innerText = "Welcome!";
    }
});

document.getElementById('trip-planner').addEventListener('click', function () {
    window.location.href = '../Trip Planner/TripPlanner.html';
});

document.getElementById('my-trips').addEventListener('click', function () {
    window.location.href = '../My Trips/MyTrips.html';
});

document.getElementById('budget-tracker').addEventListener('click', function () {
    window.location.href = '../Budget Tracker/BudgetTracker.html';
});

document.getElementById('profile-settings').addEventListener('click', function () {
    window.location.href = '../Profile Settings/Profile_Settings.html';
});

document.getElementById('logout').addEventListener('click', function () {
    localStorage.removeItem("user_name"); // Clear stored user data
    window.location.href = '../Logout/logout.html';
});
