document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission

    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();
    let errorMessage = document.getElementById("error-message");

    errorMessage.textContent = ""; // Clear any previous error

    if (email === "" || password === "") {
        errorMessage.textContent = "All fields are required!";
        return;
    }

    let formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    console.log("000", formData);

    try {
        let response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        if (response.redirected) {
            window.location.href = response.url; // Redirect to admin page
            return;
        }

        let data = await response.json();

        if (!response.ok) {
            errorMessage.textContent = data.error || "Invalid email or password!";
        }
    } catch (error) {
        console.error("Error:", error);
        errorMessage.textContent = "Something went wrong. Please try again.";
    }
});