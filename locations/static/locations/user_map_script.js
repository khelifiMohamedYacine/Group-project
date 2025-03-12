// ------------------------------------THE MAP----------------------------------------------------------
console.log("Script Successful");
var map = new maplibregl.Map({
    container: "map",
    style: "https://tiles.openfreemap.org/styles/bright",
    center: [-3.5351, 50.7371],
    zoom: 14,
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]")?.value;
}
const csrfToken = getCSRFToken();

document.addEventListener("DOMContentLoaded", async function () {
    try {
        let response = await fetch("/locations/get-locations-with-lock-status/");
        let data = await response.json();
        console.log("Fetched data:", data);

        if (!Array.isArray(data)) {
            console.error("Expected an array, but got:", data);
            return;
        }

        // Create custom HTML card to show on click
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
        card.style.pointerEvents = "auto";
        document.body.appendChild(card);

        let activeMarker = null;

        data.forEach((location) => {
            let markerColor;
            let buttonText;
            let buttonClass;
            let isDisabled = false;

            if (location.status === "locked") {
            markerColor = "red"; // Locked & Unfinished Task
            buttonText = "Check In";
            buttonClass = "btn-primary"; // Blue button for 'Check In'
            isDisabled = true; // Disable button for locked locations
            } else if (location.status === "pending") {
            markerColor = "blue"; // Unlocked & Unfinished Task
            buttonText = location.checked_in ? "Checked In" : "Check In";
            buttonClass = location.checked_in ? "btn-success" : "btn-primary";
            } else {
            markerColor = "green"; // Unlocked & Completed Task
            buttonText = "Checked In";
            buttonClass = "btn-success"; // Green button for 'Checked In'
            isDisabled = true; // Disable button for completed locations
            }

            const markerElement = new maplibregl.Marker({ color: markerColor }).setLngLat([location.longitude, location.latitude]).addTo(map);

            markerElement.getElement().addEventListener("click", function (event) {
                event.stopPropagation(); // Prevent map click event from closing the card

                if (activeMarker === markerElement) {
                    return; // Keep the card open if clicking the same marker
                }
                activeMarker = markerElement;

                let taskDetails = "";
                if (location.task1_id)
                    taskDetails += `<p>Task 1: ${location.task1_id}</p>`;
                if (location.task2_id)
                    taskDetails += `<p>Task 2: ${location.task2_id}</p>`;

                card.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${location.location_name} (ID: ${location.locID})</h5>
                        ${taskDetails}
                        <button class="btn ${
                            location.status === "locked" || location.status === "completed" ? "btn-secondary" : 
                            location.checked_in ? "btn-success" : "btn-primary"
                        } w-100 mt-2 check-in-btn" data-locid="${location.locID}" 
                        ${
                        location.status === "locked" || location.status === "completed" ? "disabled" : ""
                        } >
                        ${location.checked_in ? "Checked In" : "Check In"}
                        </button>
                    </div>
                `;

                card.style.display = "block";
                const markerPos = markerElement.getLngLat();
                const point = map.project(markerPos);

                card.style.left = `${point.x}px`;
                card.style.top = `${point.y}px`;

                // Add event listener for the check-in button
                card.querySelector(".check-in-btn").addEventListener("click", function (event) {
                    event.stopPropagation(); 
                    handleCheckIn(location);
                });
            });
        });

        // Close card on outside click
        document.addEventListener("click", function (event) {
            if (!card.contains(event.target) && !event.target.classList.contains("check-in-btn")) {
                card.style.display = "none";
                activeMarker = null;
            }
        });
    } catch (error) {
      console.error("Error fetching locations:", error);
    }
});

function handleCheckIn(location) {
    if (!navigator.geolocation) {
        alert("Geolocation is not supported by this browser.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
        const { longitude: userLongitude, latitude: userLatitude } = position.coords;
        const {
            longitude: markerLongitude,
            latitude: markerLatitude,
            locID,
        } = location;

        if (
            Math.abs(userLongitude - markerLongitude) < 0.0005 &&
            Math.abs(userLatitude - markerLatitude) < 0.0005
        ) {
            fetch(`/locations/check-in/${locID}/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ locID, checked_in: true }),
            }).then((response) => response.json()).then((data) => {
                if (data.message) {
                    updateButton(locID);
                }
            }).catch((error) =>
                console.error("Error during check-in:", error)
            );
        } else {
          alert("You are too far from the location to check in.");
        }}, () => alert("Unable to retrieve your location.")
    );
}

function updateButton(locID) {
    const button = document.querySelector(`button[data-locid="${locID}"]`);
    if (button) {
        button.textContent = "Successful!";
        button.classList.add("btn-success");
        button.classList.remove("btn-primary");
        button.disabled = true;
    }
}