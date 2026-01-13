document.addEventListener('DOMContentLoaded', function () {
  checkFlaskStatus().then((isFlaskRunning) => {
    if (isFlaskRunning) {
      fetchFilterOptions();
      fetchAttractions();

      document.getElementById('filter-city').addEventListener('change', fetchAttractions);
      document.getElementById('search-attraction').addEventListener('input', fetchAttractions);
    } else {
      loadDummyAttractions();
    }
  });
});

function checkFlaskStatus() {
  return fetch('/flask-check')
    .then(res => res.ok)
    .catch(() => false);
}

function fetchFilterOptions() {
  fetch('/api/admin/attractions/filters')
    .then(response => response.json())
    .then(data => {
      const cityFilter = document.getElementById('filter-city');
      cityFilter.innerHTML = '';

      data.cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        cityFilter.appendChild(option);
      });
    })
    .catch(error => console.error('Error fetching filter options:', error));
}

function fetchAttractions() {
  const city = document.getElementById('filter-city').value;
  const name = document.getElementById('search-attraction').value;
  const params = new URLSearchParams();

  if (city && city !== 'none') params.append('city', city);
  if (name) params.append('name', name);

  fetch('/api/admin/attractions?' + params.toString())
    .then(response => response.json())
    .then(data => displayAttractions(data))
    .catch(error => {
      console.error('Error fetching attractions:', error);
      displayErrorRow('Error loading attractions');
    });
}

function displayAttractions(attractions) {
  const tableBody = document.querySelector('#attractions-table tbody');
  tableBody.innerHTML = '';

  if (!Array.isArray(attractions) || attractions.length === 0) {
    displayErrorRow('No attractions found');
    return;
  }

  attractions.forEach(attraction => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${attraction.id}</td>
      <td>${attraction.name}</td>
      <td>${attraction.city}</td>
      <td>${attraction.zone}</td>
      <td><button onclick="deleteAttraction(${attraction.id})">Delete</button></td>
    `;
    tableBody.appendChild(row);
  });
}

function displayErrorRow(message) {
  const tableBody = document.querySelector('#attractions-table tbody');
  tableBody.innerHTML = `<tr><td colspan="5">${message}</td></tr>`;
}

function deleteAttraction(attractionId) {
  fetch(`/api/admin/attractions/delete/${attractionId}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      fetchAttractions();
    })
    .catch(error => {
      console.error('Error deleting attraction:', error);
      alert('Error deleting attraction');
    });
}

function loadDummyAttractions() {
  const tableBody = document.querySelector('#attractions-table tbody');
  tableBody.innerHTML = `
    <tr>
      <td>1</td>
      <td>Dummy Fort</td>
      <td>Jaipur</td>
      <td>North</td>
      <td><button disabled>Delete</button></td>
    </tr>
    <tr>
      <td>2</td>
      <td>Mock Museum</td>
      <td>Bengaluru</td>
      <td>East</td>
      <td><button disabled>Delete</button></td>
    </tr>
  `;

  const cityFilter = document.getElementById('filter-city');
  cityFilter.innerHTML = `
    <option value="none">none</option>
    <option value="Jaipur">Jaipur</option>
    <option value="Bengaluru">Bengaluru</option>
  `;
}
