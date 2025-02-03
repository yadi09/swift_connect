document.getElementById("check-btn").addEventListener("click", function () {
    let requestId = document.getElementById("request-id").value.trim();
    let statusResult = document.getElementById("status-result");

    if (requestId === "") {
        statusResult.textContent = "Please enter a valid Request ID.";
        statusResult.style.color = "red";
        return;
    }

    // Simulating API response with random statuses
    let statuses = ["Pending", "Approved", "Rejected"];
    let randomStatus = statuses[Math.floor(Math.random() * statuses.length)];

    statusResult.textContent = `Status: ${randomStatus}`;
    statusResult.style.color = randomStatus === "Approved" ? "green" :
        randomStatus === "Rejected" ? "red" :
            "orange";
});

// Show request form
document.getElementById("open-form-btn").addEventListener("click", function () {
    document.getElementById("request-form").style.display = "flex";
});

// Close request form
document.getElementById("close-form-btn").addEventListener("click", function () {
    document.getElementById("request-form").style.display = "none";
});

// Handle form submission
document.getElementById("submit-btn").addEventListener("click", function () {
    let companyName = document.getElementById("company-name").value.trim();
    let businessEmail = document.getElementById("business-email").value.trim();
    let swiftCode = document.getElementById("swift-code").value.trim();
    let businessType = document.getElementById("business-type").value.trim();
    let reason = document.getElementById("reason").value.trim();

    if (!companyName || !businessEmail || !swiftCode || !businessType || !reason) {
        alert("Please fill in all fields.");
        return;
    }

    alert("Request submitted successfully!");
    document.getElementById("request-form").style.display = "none";
});
