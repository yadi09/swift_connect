document.addEventListener("DOMContentLoaded", function () {
    const statusResult = document.getElementById("status-result");
    const formContainer = document.getElementById("request-form");
    const requestIdContainer = document.getElementById("request-id-container");
    const requestIdBoxText = document.getElementById("request-id-box-text");
    const copyBtn = document.getElementById("copy-btn");

    // Show request form when the open form button is clicked
    document.getElementById("open-form-btn").addEventListener("click", function () {
        formContainer.style.display = "flex";
    });

    // Close the form when the close form button is clicked
    document.getElementById("close-form-btn").addEventListener("click", function () {
        formContainer.style.display = "none";
    });

    // Handle form submission
    document.getElementById("submit-btn").addEventListener("click", async function () {
        let companyName = document.getElementById("company-name").value.trim();
        let businessEmail = document.getElementById("business-email").value.trim();
        let swiftCode = document.getElementById("swift-code").value.trim();
        let businessType = document.getElementById("business-type").value;
        let requestReason = document.getElementById("reason").value.trim();

        // Check if all fields are filled
        if (!companyName || !businessEmail || !swiftCode || !businessType || !requestReason) {
            alert("Please fill in all fields.");
            return;
        }

        try {
            // Submit the form data via fetch to the server
            let response = await fetch("/submit_request", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    company_name: companyName,
                    business_email: businessEmail,
                    swift_code: swiftCode,
                    business_type: businessType,
                    request_reason: requestReason,
                }),
            });

            let result = await response.json();
            if (result.success) {
                alert(result.message, result.request_id); // Show success message
                formContainer.style.display = "none"; // Hide form after submission

                // Clear form fields
                document.getElementById("company-name").value = "";
                document.getElementById("business-email").value = "";
                document.getElementById("swift-code").value = "";
                document.getElementById("business-type").value = "";
                document.getElementById("reason").value = "";

                // Show the Request ID copy box
                requestIdBoxText.textContent = result.request_id; // Display the Request ID from server response
                requestIdContainer.style.display = "block"; // Make the box visible
            } else {
                alert(result.message); // Show error message if submission fails
            }
        } catch (error) {
            console.error("Error submitting request:", error);
            alert("Something went wrong. Please try again.");
        }
    });

    // Copy Request ID to clipboard when the copy button is clicked
    copyBtn.addEventListener("click", function () {
        const range = document.createRange();
        range.selectNode(requestIdBoxText);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand("copy"); // Copy text to clipboard

        // Show confirmation message
        alert("Request ID copied to clipboard!");
    });
});
