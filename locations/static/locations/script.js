var map = new maplibregl.Map({
  container: "map",
  style: "https://tiles.openfreemap.org/styles/bright",
  center: [-3.5351, 50.7371],
  zoom: 14,
});

function getCSRFToken() {
  const csrfToken = document
    .querySelector("[name=csrf-token]")
    .getAttribute("content");
  return csrfToken;
}

//To handle the parent location button
document.addEventListener("DOMContentLoaded", function () {
  // Get the task dropdown and button elements
  const parentLocationBtn = document.getElementById(
    "selectedParentLocationBtn"
  );
  const parentLocationInput = document.getElementById("parentLocationInput");

  // Event listener for selecting a parent location
  document.querySelectorAll(".parent-location-option").forEach((item) => {
    item.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent page refresh

      // Get the locID and location name from the clicked item
      let selectedId = this.getAttribute("data-id"); // ✅ Get locID
      let selectedName = this.textContent.trim(); // ✅ Get full text (name + ID)

      // Update the dropdown button text
      parentLocationBtn.textContent = selectedName;

      // Store the locID in the hidden input field (ensuring locID is sent to backend)
      parentLocationInput.value = selectedId;

      console.log("Locked By (hidden input value - locID):", selectedId); // Debugging output
    });
  });
});

//--------------------------------------------------------------------------------------------
//To handle the task buttons
document.addEventListener("DOMContentLoaded", function () {
  // Handle Task 1 selection
  const task1Btn = document.getElementById("selectedTask1Btn");
  const task1Input = document.getElementById("task1Input");

  // Event listener for Task 1 dropdown options
  document.querySelectorAll("#task1Dropdown .task-option").forEach((item) => {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      let selectedTaskId = this.getAttribute("data-id");
      let selectedTaskName = this.getAttribute("data-name");

      // Update Task 1 button text
      task1Btn.textContent = selectedTaskName;

      // Store Task 1 ID in hidden input
      task1Input.value = selectedTaskId;
    });
  });

  // Handle Task 2 selection
  const task2Btn = document.getElementById("selectedTask2Btn");
  const task2Input = document.getElementById("task2Input");

  // Event listener for Task 2 dropdown options
  document.querySelectorAll("#task2Dropdown .task-option").forEach((item) => {
    item.addEventListener("click", function (event) {
      event.preventDefault();
      let selectedTaskId = this.getAttribute("data-id");
      let selectedTaskName = this.getAttribute("data-name");

      // Update Task 2 button text
      task2Btn.textContent = selectedTaskName;

      // Store Task 2 ID in hidden input
      task2Input.value = selectedTaskId;
    });
  });
});

//-----------------------------------------------------------------------------------------------------------
// Getting the saved locations from the database
document.addEventListener("DOMContentLoaded", async function () {
  try {
    let response = await fetch("/get-locations/");
    let data = await response.json();
    console.log("Fetched data:", data);

    if (!Array.isArray(data)) {
      console.error("Expected an array, but got:", data);
      return;
    }

    // Create custom HTML card to show on hover
    const card = document.createElement("div");
    card.className = "card";
    card.style.display = "none";
    card.style.position = "absolute";
    card.style.width = "18rem";
    card.style.backgroundColor = "white";
    card.style.border = "1px solid #ccc";
    card.style.borderRadius = "5px";
    card.style.boxShadow = "2px 2px 10px rgba(0, 0, 0, 0.2)";
    card.style.padding = "10px";
    card.style.zIndex = "10";
    card.style.pointerEvents = "none";

    document.body.appendChild(card);

    // Add markers for stored locations
    data.forEach((location, index) => {
      const markerElement = new maplibregl.Marker()
        .setLngLat([location.longitude, location.latitude])
        .addTo(map);

      // Set hover event to show the card
      markerElement.getElement().addEventListener("mouseenter", function () {
        card.style.display = "block";

        // Build task list dynamically
        let taskDetails = "";
        if (location.task1) taskDetails += `<p>Task 1: ${location.task1}</p>`;
        if (location.task2) taskDetails += `<p>Task 2: ${location.task2}</p>`;

        // Set card content dynamically based on the available data
        card.innerHTML = `
                <div class="card-body">
                <h5 class="card-title">${location.location_name} (ID: ${location.locID})</h5>
                ${taskDetails} 
                </div>
            `;

        // Position the card relative to the marker
        const markerPos = markerElement.getLngLat();
        const point = map.project(markerPos); // Convert geographic coordinates to pixels

        // Adjust the card position to be closer to the marker
        const offsetX = 0.05;
        const offsetY = -0.05;

        card.style.left = `${point.x + offsetX}px`;
        card.style.top = `${point.y + offsetY}px`;
      });

      // Set hover event to hide the card
      markerElement.getElement().addEventListener("mouseleave", function () {
        card.style.display = "none";
      });
    });
  } catch (error) {
    console.error("Error loading saved locations:", error);
  }
});

//---------------------------------------------------------------------------------------------------------------------
let selectedCoordinates = { lat: 9999, lon: 9999 }; // Default values that represent no input

document
  .getElementById("floatingPostcode")
  .addEventListener("input", async function () {
    //Auto-fill the Address bar after the user enters the postcode
    let postcode = this.value.trim();
    if (postcode.length >= 5) {
      try {
        let response = await fetch(
          `https://api.postcodes.io/postcodes/${postcode}`
        );
        let data = await response.json();
        if (data.status === 200) {
          let result = data.result;

          let fullAddress = [
            result.thoroughfare,
            result.street,
            result.dependent_thoroughfare,
            result.admin_district,
            result.post_town,
            result.region,
            result.country,
          ]
            .filter(Boolean)
            .join(", ");
          document.getElementById("floatingAddress").value =
            fullAddress || "Unknown Address";
          selectedCoordinates = {
            lat: result.latitude,
            lon: result.longitude,
          };
          map.flyTo({
            //Fly to the location after the user enters the postcode
            center: [selectedlatitudeCoordinates.lon, selectedCoordinates.lat],
            zoom: 12,
          });
        }
      } catch (error) {
        console.error("Error fetching postcode data:", error);
      }
    }
  });

//---------------------------------------------------------------------------------------------------------------

let lastMarker = null;
document.addEventListener("DOMContentLoaded", function () {
  // Listen for map click to get coordinates and auto-fill address
  map.on("click", async function (e) {
    const clickedLngLat = e.lngLat;

    // Remove the last marker if it exists
    if (lastMarker) {
      lastMarker.remove();
    }

    // Fetch the nearest postcode from the coordinates using Postcodes.io
    try {
      const response = await fetch(
        `https://api.postcodes.io/postcodes?lat=${clickedLngLat.lat}&lon=${clickedLngLat.lng}`
      );
      const data = await response.json();

      // Add the marker directly using the clicked coordinates
      lastMarker = new maplibregl.Marker({ color: "red" })
        .setLngLat([clickedLngLat.lng, clickedLngLat.lat])
        .addTo(map);

      if (data.result && data.result.length > 0) {
        const postcode = data.result[0].postcode; // Get the postcode from the result

        // Now use the postcode to get the full address
        const addressResponse = await fetch(
          `https://api.postcodes.io/postcodes/${postcode}`
        );
        const addressData = await addressResponse.json();

        if (addressData.result) {
          const result = addressData.result;

          // Build the address string by checking the availability of address components
          const line1 = result.line_1 || "";
          const line2 = result.line_2 ? `${result.line_2}, ` : "";
          const city = result.city || "";
          const county = result.county || "";
          const country = result.country || "";

          const fullAddress = `${line1} ${line2}${city} ${county} ${country}`
            .trim()
            .replace(/, +$/, ""); // Remove any trailing comma

          // Auto-fill the fields with the retrieved address and postcode
          document.getElementById("floatingAddress").value = fullAddress;
          document.getElementById("floatingPostcode").value = postcode;

          // Save the coordinates
          selectedCoordinates = {
            lat: clickedLngLat.lat,
            lon: clickedLngLat.lng,
          };
        } else {
          alert("Address not found for the selected postcode.");
        }
      } else {
        // If postcode is not found, still add the marker using the clicked coordinates
        selectedCoordinates = {
          lat: clickedLngLat.lat,
          lon: clickedLngLat.lng,
        };
        // Instead of leaving it empty, assign "Not Available" to the postcode field
        document.getElementById("floatingPostcode").value = "Not Available";
        document.getElementById("floatingAddress").value =
          "Address not available";
      }
    } catch (error) {
      console.error("Error fetching address:", error);
      alert("Failed to retrieve address for the selected location.");
      // If error occurs, set postcode as 'Not Available'
      document.getElementById("floatingPostcode").value = "Not Available";
    }
  });
  //--------------------------------------------------------------------------------------------------------------

  //Add marker when the user presses the button. Already saved locations will be in blue, new ones added will be in red
  document
    .getElementById("addLocationBtn")
    .addEventListener("click", async function () {
      let postcode = document.getElementById("floatingPostcode").value.trim();
      let address = document.getElementById("floatingAddress").value.trim();
      let locationName = document
        .getElementById("floatingLocationName")
        .value.trim();

      let lockedBy = document.getElementById("parentLocationInput")
        ? document.getElementById("parentLocationInput").value || null
        : null;

      // Check if the task input elements exist otherwise set to null
      let task1Id = document.getElementById("task1Input")
        ? document.getElementById("task1Input").value || null
        : null;
      let task2Id = document.getElementById("task2Input")
        ? document.getElementById("task2Input").value || null
        : null;

      let response = await fetch("/add-location/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          postcode: postcode,
          address: address,
          location_name: locationName,
          latitude: selectedCoordinates.lat,
          longitude: selectedCoordinates.lon,
          task1: task1Id,
          task2: task2Id,
          locked_by: lockedBy,
        }),
      });
      let result = await response.json();

      if (response.ok) {
        // Only add the marker if the response is successful
        new maplibregl.Marker({ color: "red" })
          .setLngLat([selectedCoordinates.lon, selectedCoordinates.lat])
          .addTo(map);
        alert("Location added successfully!");
      } else if (response.status === 400) {
        // Input validation errors now handled on the backend for consistency and security
        alert(result.error);
      } else {
        alert("An error occurred while adding the location.");
      }
    });
});
