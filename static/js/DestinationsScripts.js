document.addEventListener('DOMContentLoaded', function() { 
    fetchDestinations();
    fetchFilterOptions();
    document.getElementById('add-destination-form').addEventListener('submit', function(event) {
      event.preventDefault();
      addDestination();
    });
  });
  
  function fetchDestinations(filters = {}) {
    const searchName = document.getElementById('search-destination').value;
    const city = document.getElementById('filter-city').value;
    const country = document.getElementById('filter-country').value;
  
    if (searchName) filters.name = searchName;
    if (city) filters.city = city;
    if (country) filters.country = country;
  
    fetch('/api/admin/destinations?' + new URLSearchParams(filters))
      .then(response => response.json())
      .then(data => {
        const tableBody = document.querySelector('#destinations-table tbody');
        tableBody.innerHTML = '';
        data.forEach(destination => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${destination.destination_id}</td>
            <td>${destination.city}</td>
            <td>${destination.country}</td>
            <td><button onclick="deleteDestination('${destination.destination_id}')">Delete</button></td>
          `;
          tableBody.appendChild(row);
        });
      })
      .catch(error => console.error('Error fetching destinations:', error));
  }
  
  function deleteDestination(id) {
    fetch(`/admin/destinations/delete/${id}`, { method: 'DELETE' })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        fetchDestinations();
      })
      .catch(error => console.error('Error deleting destination:', error));
  }
  