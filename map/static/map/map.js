document.addEventListener('DOMContentLoaded', function () {

    // Locations as HTML content 
    const locations = {
        loc1: document.getElementById("loc1"),
        loc2: document.getElementById("loc2"),
        loc3: document.getElementById("loc3"),
        loc4: document.getElementById("loc4"),
        loc5: document.getElementById("loc5"),
        loc6: document.getElementById("loc6"),
        loc7: document.getElementById("loc7"),
        loc8: document.getElementById("loc8")
    };

    // Dependency graph for locations
    const locationGraph = {
        loc1: ['loc3'],         // Unlocking loc1 unlocks loc3
        loc2: ['loc4', 'loc5'], // Unlocking loc2 unlocks loc4 and loc5
        loc3: ['loc6'],         // Unlocking loc3 unlocks loc6
        loc4: ['loc6', 'loc7'], // Unlocking loc4 unlocks loc6 and loc7
        loc5: ['loc6', 'loc7'], // Unlocking loc5 unlocks loc6 and loc7
        loc6: ['loc8'],         // Unlocking loc6 unlocks loc8
        loc7: ['loc8'],         // Unlocking loc7 unlocks loc8
        loc8: []                // loc8 has no further dependencies
    };

    // Counter for unlocked locations
    let unlockedCount = 0;

    // Function to enable the checkbox (turning it into an active switch)
    function enableCheckbox(locationId) {
        const checkbox = document.querySelector(`#${locationId} .form-check-input`);
        const label = document.querySelector(`#${locationId} .form-check-label`);
        if (checkbox) {
            checkbox.disabled = false;  // Enable the checkbox
            label.textContent = `Unlock ${locationId}`;
            changeIconColor(locationId, 'blue'); // Set the icon color to blue (disabled)
        }
    }

    // Function to change the icon color based on location state
    function changeIconColor(locationId, color) {
        const icon = document.querySelector(`#${locationId} svg`);
        if (icon) {
            icon.setAttribute('fill', color);
        }
    }

    // Function to unlock the locations when checkbox is checked
    function unlockLocation(unlockedLocation) {
        const checkbox = document.querySelector(`#${unlockedLocation} .form-check-input`);
        if (checkbox && checkbox.checked) {
            locationGraph[unlockedLocation]?.forEach(nextLocation => {
                const nextCheckbox = document.querySelector(`#${nextLocation} .form-check-input`);
                if (nextCheckbox && nextCheckbox.disabled) {
                    enableCheckbox(nextLocation); 
                    changeIconColor(nextLocation, 'blue'); 
                }
            });
        }
    }

    // Function to handle checkbox toggle
    function handleCheckboxChange(event, locationId) {
        const checkbox = event.target;
        if (checkbox.checked) {
            unlockLocation(locationId);  // Unlock related locations when checked
            changeIconColor(locationId, 'green'); // Change to green color when checked
            unlockedCount++; // Increment the unlocked counter
        } else {
            changeIconColor(locationId, 'blue'); // Change back to blue if unchecked
            unlockedCount--; // Decrement the counter if unchecked
        }

        // Check if the counter has reached 8
        if (unlockedCount === 8) {
            window.location.href = "certificate.url";  // Replace with your CERTIFICATE URL
        }
    }

    // Attach event listeners to the checkboxes
    document.querySelectorAll('.form-check-input').forEach((checkbox) => {
        const locationId = checkbox.closest('.location').id;  
        checkbox.addEventListener('change', (event) => handleCheckboxChange(event, locationId));
    });

    // Initially disable all locations except loc1 and loc2
    ['loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8'].forEach(locationId => {
        const checkbox = document.querySelector(`#${locationId} .form-check-input`);
        if (checkbox) {
            checkbox.disabled = true;
            checkbox.checked = false; 
            changeIconColor(locationId, 'red'); 
        }
    });

    // Enable loc1 and loc2 initially
    enableCheckbox('loc1');
    enableCheckbox('loc2');
    changeIconColor('loc1', 'blue'); 
    changeIconColor('loc2', 'blue'); 

});