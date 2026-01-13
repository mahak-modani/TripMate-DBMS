document.getElementById('budget-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission?

    const transportation = parseFloat(document.getElementById('transportation').value) || 0;
    const accommodation = parseFloat(document.getElementById('accommodation').value) || 0;
    const food = parseFloat(document.getElementById('food').value) || 0;
    const activities = parseFloat(document.getElementById('activities').value) || 0;

    const totalBudget = transportation + accommodation + food + activities;

    document.getElementById('total-budget').textContent = totalBudget.toFixed(2);
});
