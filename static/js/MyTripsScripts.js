document.addEventListener("DOMContentLoaded", function () {
    checkIfFlaskRunning().then(isFlaskRunning => {
        updateSidebarLinks(isFlaskRunning);
        fetchTrips(isFlaskRunning);
    });
});

// Function to check if Flask is running
async function checkIfFlaskRunning() {
    try {
        const response = await fetch("/flask-check");
        return response.ok;
    } catch (error) {
        return false; // If an error occurs, assume Flask is NOT running
    }
}

// Update sidebar links based on Flask status
function updateSidebarLinks(isFlaskRunning) {
    const links = {
        "dashboard": isFlaskRunning ? "/dashboard" : "../templates/dashboard.html",
        "trip-planner": isFlaskRunning ? "/trip_planner" : "../templates/TripPlanner.html",
        "my-trips": isFlaskRunning ? "/my_trips" : "../templates/MyTrips.html",
        "budget-tracker": isFlaskRunning ? "/budget_tracker" : "../templates/BudgetTracker.html",
        "profile-settings": isFlaskRunning ? "/profile_settings" : "../templates/Profile_Settings.html",
        "logout": isFlaskRunning ? "/logout" : "../templates/logout.html"
    };

    Object.keys(links).forEach(id => {
        document.getElementById(id).setAttribute("href", links[id]);
    });
}

// Default trip data if Flask is not running
const defaultTrips = [
    {
        trip_id: "DEFAULT1",
        city: "Paris",
        country: "France",
        start_date: "2024-03-15",
        end_date: "2024-03-20",
        accommodation_type: "Hotel",
        accommodation_cost: 500.00,
        transportation_type: "Flight",
        transportation_cost: 300.00,
        budget: 1200.00
    },
    {
        trip_id: "DEFAULT2",
        city: "Tokyo",
        country: "Japan",
        start_date: "2023-12-05",
        end_date: "2023-12-12",
        accommodation_type: "Hostel",
        accommodation_cost: 250.00,
        transportation_type: "Train",
        transportation_cost: 100.00,
        budget: 800.00
    }
];

// Fetch trips from API or use default data
async function fetchTrips(isFlaskRunning) {
    if (isFlaskRunning) {
        try {
            const response = await fetch("/api/user/my_trips", { credentials: "include" });

            const trips = await response.json();

            if (trips.error) {
                console.error("Error:", trips.error);
                displayTrips(defaultTrips, false); // Show default trips if unauthorized
            } else {
                displayTrips(trips, true);
            }
        } catch (error) {
            console.error("Error fetching trips:", error);
            displayTrips(defaultTrips, false);
        }
    } else {
        displayTrips(defaultTrips, false);
    }
}

// Function to display trips on the page
function displayTrips(trips) {
    const container = document.getElementById("trip-container");
    container.innerHTML = ""; // Clear previous content

    if (trips.length === 0) {
        displayNoTripsMessage();
        return;
    }

    trips.forEach(trip => {
        const tripCard = document.createElement("div");
        tripCard.classList.add("trip-card");
        tripCard.innerHTML = `
            <h3>${trip.city}, ${trip.country}</h3>
            <p><strong>Trip ID:</strong> ${trip.trip_id}</p>
            <p><strong>Start Date:</strong> ${trip.start_date}</p>
            <p><strong>End Date:</strong> ${trip.end_date}</p>
            <p><strong>Accommodation:</strong> ${trip.accommodation_type} ($${trip.accommodation_cost.toFixed(2)})</p>
            <p><strong>Transportation:</strong> ${trip.transportation_type} ($${trip.transportation_cost.toFixed(2)})</p>
            <p><strong>Budget:</strong> $${trip.budget.toFixed(2)}</p>
        `;
        container.appendChild(tripCard);
    });
}

// Function to show "No Trips Found" message
function displayNoTripsMessage() {
    const container = document.getElementById("trip-container");
    container.innerHTML = `<p class="no-trips">No trips found. Plan your first trip!</p>`;
}
