document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let errorMessage = document.getElementById("error-message");

    errorMessage.textContent = ""; // Clear any previous error

    if (email === "" || password === "") {
        errorMessage.textContent = "All fields are required!";
        return;
    }

    // Mock Login Validation (Replace with actual API request)
    if (email === "admin@example.com" && password === "admin123") {
        alert("Login Successful!");
        window.location.href = "dashboard.html"; // Redirect after login
    } else {
        errorMessage.textContent = "Invalid email or password.";
    }
});
