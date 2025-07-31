document.addEventListener("DOMContentLoaded", () => { // Wait for the DOM to load
    function isTokenExpired(token) {
        try {
            const payload = JSON.parse(atob(token.split(".")[1]));
            const now = Math.floor(Date.now() / 1000);
            return payload.exp < now;
        } catch (e) {
            return true; // if token is malformed, treat as expired
        }
    }

    const token = localStorage.getItem("token");
    if (token && !isTokenExpired(token)) {
        window.location.href = BASE_URL + "/events";
        return;
    } else {
        localStorage.removeItem("token"); // Remove expired/invalid token
    }
    // Add event listener to login form
    document.getElementById("loginForm").addEventListener("submit", async (e) => {
        e.preventDefault(); // Prevent default form submission

        // Extract values from the form fields, for user login
        const username = document.querySelector("#email").value;
        const password = document.querySelector("#password").value;

        // Send a POST request to the API login endpoint
        const res = await fetch(BASE_URL + "/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                username,
                password
            })
        });

        // If the response is OK, extract the token from the response and save it to localStorage
        // Redirect to events page
        if (res.ok) {
            const data = await res.json();
            localStorage.setItem("token", data.access_token); // Save token
            window.location.href = BASE_URL + "/events"; 
        } else { // Otherwise, display an error message.
            document.getElementById("response").innerText = "Login failed.";
        }
    });
});