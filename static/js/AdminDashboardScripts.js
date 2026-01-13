document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/admin/dashboard/stats')
        .then(response => response.json())
        .then(data => {
            console.log("Fetched data:", data);  // Log the response data for debugging
  
            // Check if the expected keys exist before updating the page
            if (data.totalUsers !== undefined) {
                document.querySelector('#total-users').textContent = `Total Users: ${data.totalUsers}`;
            }
            if (data.totalDestinations !== undefined) {
                document.querySelector('#total-destinations').textContent = `Total Destinations: ${data.totalDestinations}`;
            }
            if (data.totalAttractions !== undefined) {
                document.querySelector('#total-attractions').textContent = `Total Attractions: ${data.totalAttractions}`;
            }
            if (data.totalTrips !== undefined) {
                document.querySelector('#total-trips').textContent = `Total Trips: ${data.totalTrips}`;
            }
            if (data.totalBudgets !== undefined) {
                document.querySelector('#total-budgets').textContent = `Total Budgets: ₹${data.totalBudgets}`;
            }
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
  });
  