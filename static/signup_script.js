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
        window.location.href = "http://localhost:8000/events";
        return;
    } else {
        localStorage.removeItem("token"); // Remove expired/invalid token
    }
    // Add event listener to signup form
    document.getElementById("signupForm").addEventListener("submit", async (e) => { 
        e.preventDefault(); // Prevent default form submission
        // Extract values from the form fields
        const username = document.querySelector("#username").value;
        const email = document.querySelector("#email").value;
        const password = document.querySelector("#password").value;
        
        // Send a POST request to the API signup endpoint
        const res = await fetch("http://localhost:8000/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({username, email, password}),
        })

        // If the response is OK, redirect to login page;
        if(res.ok){
            window.location.href = "http://localhost:8000/login";
        }
        
        // Otherwise, display an error message.
        else {
            document.getElementById("response").innerText = "Signup failed. Please check information and try again.";
        }
    });
});