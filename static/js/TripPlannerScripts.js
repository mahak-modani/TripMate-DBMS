document.addEventListener('DOMContentLoaded', () => {
    const countrySelect = document.getElementById('country');
    const citySelect = document.getElementById('city');
    const areaSelect = document.getElementById('area');
    const attractionSearch = document.getElementById('attraction-search');
    const addToItineraryBtn = document.getElementById('add-to-itinerary');
    const itineraryList = document.getElementById('itinerary-list');
    const saveItineraryBtn = document.getElementById('save-itinerary');
    const warningBanner = document.getElementById('warning-banner');
    const budgetInput = document.getElementById('budget');
    const totalExpensesElement = document.getElementById('total-expenses');
    const remainingBudgetElement = document.getElementById('remaining-budget');
    const generateItineraryBtn = document.getElementById('generate-itinerary');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const transportModeSelect = document.getElementById('transport-mode');

    // Check essential elements before continuing
    if (!budgetInput || !generateItineraryBtn || !citySelect || !countrySelect || !areaSelect || !startDateInput || !endDateInput || !transportModeSelect || !itineraryList || !totalExpensesElement || !remainingBudgetElement) {
        console.warn("Some required elements are missing. Make sure all form fields and buttons exist in your HTML.");
        return;
    }

    let itineraryData = [];
    let totalExpenses = 0;
    let userBudget = 0;
    let tripId = null;

    // Always start fresh — no localStorage
    budgetInput.value = "";
    updateBudgetDisplay();

    function updateBudgetDisplay() {
        const remainingBudget = userBudget - totalExpenses;
        remainingBudgetElement.textContent = `$${remainingBudget.toFixed(2)}`;
        totalExpensesElement.textContent = `$${totalExpenses.toFixed(2)}`;
        warningBanner.style.display = remainingBudget < 0 ? 'block' : 'none';
    }

    budgetInput.addEventListener('change', () => {
        userBudget = parseFloat(budgetInput.value) || 0;
        updateBudgetDisplay();

        const city = citySelect.value;
        const country = countrySelect.value;
        const area = areaSelect.value;
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const transportMode = transportModeSelect.value;

        if (userBudget && city && area && startDate && endDate && transportMode) {
            generateItineraryBtn.click();
        }
    });

    countrySelect.addEventListener('change', function () {
        const country = this.value;
        if (country) {
            citySelect.disabled = false;
            citySelect.innerHTML = `<option value="">Select City</option>`;
            const cities = country === "India" ? ["Jaipur", "Bengaluru"] : [];
            cities.forEach(city => {
                citySelect.innerHTML += `<option value="${city}">${city}</option>`;
            });
        } else {
            citySelect.disabled = true;
            areaSelect.disabled = true;
        }
    });

    citySelect.addEventListener('change', function () {
        const city = this.value;
        if (city) {
            areaSelect.disabled = false;
            areaSelect.innerHTML = `<option value="">Select Area</option>`;
            const areas = ["Area 1", "Area 2"];
            areas.forEach(area => {
                areaSelect.innerHTML += `<option value="${area}">${area}</option>`;
            });
        } else {
            areaSelect.disabled = true;
        }
    });

    generateItineraryBtn.addEventListener('click', async () => {
        const budget = parseFloat(budgetInput.value);
        const city = citySelect.value;
        const country = countrySelect.value;
        const area = areaSelect.value;
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const transportMode = transportModeSelect.value;

        if (!budget || !city || !area || !startDate || !endDate) {
            alert("Please fill all fields before generating.");
            return;
        }

        try {
            const response = await fetch("/api/user/generate_itinerary", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: "U1",
                    trip_id: tripId,
                    city: city,
                    area: area,
                    start_date: startDate,
                    end_date: endDate,
                    budget: budget,
                    transport_mode: transportMode
                })
            });

            const data = await response.json();
            console.log("Received itinerary data:", data);

            itineraryData = data.itinerary;
            totalExpenses = data.budget_used;
            userBudget = budget;
            if (data.trip_id) {
                tripId = data.trip_id; // Cache the trip ID
            }
            document.getElementById('generated-itinerary').style.display = 'block';

            updateItineraryDisplay();
            updateBudgetDisplay();
        } catch (error) {
            console.error("Error fetching itinerary:", error);
            alert("Failed to generate itinerary. Please try again.");
        }
    });

    function updateItineraryDisplay() {
        itineraryList.innerHTML = "";

        if (itineraryData.length === 0) {
            itineraryList.innerHTML = "<p>No itinerary could be generated within the budget.</p>";
            return;
        }

        let currentDay = "";
        itineraryData.forEach(item => {
            if (item.visit_date !== currentDay) {
                currentDay = item.visit_date;
                const dayHeader = document.createElement("h3");
                dayHeader.className = "day-heading";
                dayHeader.textContent = `Day - ${currentDay}`;
                itineraryList.appendChild(dayHeader);
            }

            const itemDiv = document.createElement("div");
            itemDiv.className = "itinerary-item";
            itemDiv.innerHTML = `
                <p><strong>Attraction:</strong> ${item.name}</p>
                <p><strong>Significance:</strong> ${item.significance}</p>
                <p><strong>Time of Day:</strong> ${item.visit_time}</p>
                <p><strong>Transportation:</strong> ${item.transport_mode}</p>
                <p><strong>Travel Time:</strong> ${item.travel_time} mins</p>
                <p><strong>Attraction Fee:</strong> ₹${item.fee}</p>
                <p><strong>Transport Fee:</strong> ₹${item.transport_cost}</p>
            `;
            itineraryList.appendChild(itemDiv);

            const hr = document.createElement("hr");
            itineraryList.appendChild(hr);
        });
    }

    saveItineraryBtn?.addEventListener('click', () => {
        if (itineraryData.length > 0 && totalExpenses <= userBudget) {
            alert('Your itinerary has been saved!');
        } else {
            warningBanner.style.display = 'block';
        }
    });
});
