function isTokenExpired(token) {
    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        const now = Math.floor(Date.now() / 1000);
        return payload.exp < now;
    } catch (e) {
        return true; // if token is malformed, treat as expired
    }
}

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem("token");

    if (!token || isTokenExpired(token)) {
        localStorage.removeItem("token");
        window.location.href = BASE_URL + "/login";
        return Promise.reject("Token expired or missing. Redirecting...");
    }

    const authHeaders = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
    };

    const updatedOptions = {
        ...options,
        headers: authHeaders,
    };

    return fetch(url, updatedOptions);
}


document.addEventListener("DOMContentLoaded", async () => { // Wait for the DOM to load
    // Check if user is authenticated
    const token = localStorage.getItem("token");
    if (!token || isTokenExpired(token)) {
        localStorage.removeItem("token"); // Remove expired/invalid token
        window.location.href = BASE_URL + "/login";
        return;
    } 

    await loadUserEvents(); // Load user events on page load
    await loadCurrentUser(); // Load current user info

    // Add event listener to events form
    document.getElementById("eventForm").addEventListener("submit", async (e) => { 
        e.preventDefault(); // Prevent default form submission
        // Extract data from form
        const name = document.querySelector("#name").value;
        const description = document.querySelector("#description").value;
        const date = document.querySelector("#date").value;
        const duration = document.querySelector("#duration").value;

        // Call API endpoint to create an event with the form data, demand token
        const res = await fetchWithAuth(BASE_URL + "/events", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json"
            },
            body: JSON.stringify({name, description, date, duration}),
        });
        console.log(JSON.stringify({name, description, date, duration}));
        const data = await res.json();
        document.getElementById("response").innerText = data.message;
        if(res.ok) {
            e.target.reset(); // Reset the form
            await loadUserEvents(); // Reload events after successful submission
            await loadCurrentUser(); // Reload current user info
        }
    });
});

// Function to generate the list of events of the current logged in user, as well as update and delete options for each.
async function loadUserEvents() { 

    // Call API endpoint to fetch the current user's events, user id extracted from token (see oauth2.py).
    const res = await fetchWithAuth(BASE_URL + "/events/show", { 
        method: "GET",
        headers: { 
            "Content-Type": "application/json"
        }
    });

    // If the response is okay, proceed with generating the list
    if (res.ok) {
        const events = await res.json(); // Place it into events
        console.log("Events loaded:", events); // Log into console, for debug

        const eventList = document.getElementById("eventList"); // Create the eventList object from HTML
        eventList.innerHTML = "";

        events.forEach((event) => { // Add a list element to it for each event extracted before
            const li = document.createElement("li");
            li.innerHTML = `
                <strong>${event.name}</strong><br>
                Description: ${event.description}<br>
                Date: ${event.date}<br>
                Duration: ${event.duration} hours<br>
            `;

            // Update event button, generated for each event listed
            const updateBtn = document.createElement("button");
            updateBtn.textContent = "Update";
            // Add a click event listener
            updateBtn.addEventListener("click", async () => {
                // Prompt the user to update the properties, save them
                const newName = prompt("Enter new name:", event.name);
                const newDescription = prompt("Enter new description:", event.description);
                const newDate = prompt("Enter new date (YYYY-MM-DDTHH:MM):", event.date);
                const newDuration = prompt("Enter new duration:", event.duration);
                
                // Call the API endpoint if the data is introduced, updating this specific event.
                if (newName && newDescription && newDate && newDuration) {
                    const updateRes = await fetchWithAuth(BASE_URL + `/events/${event.id}`, {
                        method: "PUT",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        // Convert data for the body to JSON
                        body: JSON.stringify({
                            name: newName,
                            description: newDescription,
                            date: newDate,
                            duration: parseInt(newDuration)
                        })
                    });

                    if (updateRes.ok) {
                        await loadUserEvents(); // Reload the events if the update happened
                    } else {
                        console.error("Update failed");
                    }
                }
            });

            // Delete event button, generated for each event listed
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            // Add a click event listener
            deleteBtn.addEventListener("click", async () => {
                // Call the API endpoint to delete the specific event
                const delRes = await fetchWithAuth(BASE_URL + `/events/${event.id}`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json"
                    } // Despite the events being listed are already validated as belonging to the logged in user,
                    // it's good practice to check the token for both the update and delete.
                });

                if (delRes.ok) {
                    await loadUserEvents(); // Reload the events list after deletion
                } else {
                    console.error("Delete failed");
                }
            });

            li.appendChild(updateBtn); // Actually append the update and delete buttons
            li.appendChild(deleteBtn);
            eventList.appendChild(li); // And the event item itself.
        });
    } else {
        console.error("Could not load events.");
    }
}

// Function to load the current user, and actions regarding the user.
async function loadCurrentUser() {
    // Check for a token. If there is none, there is no logged user.
    const token = localStorage.getItem("token"); 
    if (!token || isTokenExpired(token)) {
        console.error("No token found, or is expired");
        return;
    }

    // Get the current user's username through an API route, extracting it from the token.
    const res = await fetchWithAuth(BASE_URL + "/users/current", { 
        method: "GET",
        headers: { 
            "Content-Type": "application/json"
        }
    });

    // Create the delete user button constant
    const deleteUserBtn = document.getElementById("deleteUserBtn");
    deleteUserBtn.style.display = "block"; // Show delete button
    // To prevent constant initialization on each refresh, a boolean variable is introduced and set to true after initialization.
    if (!deleteUserBtn.dataset.initialized){
        // Add a click event listener to the delete user button.
        deleteUserBtn.addEventListener("click", async () => {
            // Prompt a confirmation
            const confirmDelete = confirm("Are you sure you want to delete your account?");
            if (confirmDelete) {
                // If confirmed, call API endpoint to delete the user. It will extract the user from the token in the backend.
                const delRes = await fetchWithAuth(BASE_URL + `/users/delete`, {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                
                // If deletion worked, remove the token, redirect to login.
                if (delRes.ok) {
                    alert("Account deleted successfully.");
                    localStorage.removeItem("token");
                    window.location.href = BASE_URL + "/login"; // Redirect to login page
                } else {
                    console.error("Account deletion failed.");
                }
            }
        });
        deleteUserBtn.dataset.initialized = true; // Mark as initialized
    }

    // Create the log out button constant
    const logoutBtn = document.getElementById("logoutBtn");
    // Add the click event listener
    logoutBtn.addEventListener("click", () => {
        // On log out, since all operations use the token for authentication, just remove the token and redirect.
        localStorage.removeItem("token");
        window.location.href = BASE_URL + "/login"; // Redirect to login page
    });

    // Finally, use the username returned by the first endpoint call within this function.
    if (res.ok) {
        const user = await res.json();
        document.getElementById("currentUser").innerText = `Logged in as: ${user.username}`;
    } else {
        console.error("Could not load current user.");
    }
}