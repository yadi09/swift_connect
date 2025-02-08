document.addEventListener("DOMContentLoaded", function () {
    const statusResult = document.getElementById("status-result");
    const formContainer = document.getElementById("request-form");
    const requestIdContainer = document.getElementById("request-id-container");
    const requestIdBoxText = document.getElementById("request-id-box-text");
    const copyBtn = document.getElementById("copy-btn");
    const statusBox = document.getElementById("status-box");
    const checkBtn = document.getElementById("check-btn");
    const requestIdInput = document.getElementById("request-id");
    const statusText = document.getElementById("status-text");

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


    // Handle "Check" button click
    checkBtn.addEventListener("click", async function () {
        const requestId = requestIdInput.value.trim(); // Get the entered request ID

        // Check if the request ID is entered
        console.log(requestId);
        if (!requestId) {
            alert("Please enter a valid Request ID.");
            return;
        }

        try {
            let response = await fetch("/get_request/" + requestId);
            console.log("0101010", response);
            let data = await response.json();
            console.log("000000", data);

            if (data.success) {
                // Populate the status box with the request details
                console.log("11111111111", data);
                document.getElementById('status-company').textContent = data.company_name || 'N/A';
                document.getElementById('status-email').textContent = data.business_email || 'N/A';
                document.getElementById('status-swift').textContent = data.swift_code || 'N/A';
                document.getElementById('status-business-type').textContent = data.business_type || 'N/A';
                document.getElementById('status-reason').textContent = data.request_reason || 'N/A';
                document.getElementById('status-text').textContent = data.request_status || 'N/A';

                // Remove any existing status class
                statusText.classList.remove("pending", "approved", "rejected");

                // Apply the appropriate status class based on request status
                if (data.request_status.toLowerCase() === "pending") {
                    statusText.classList.add("pending");
                } else if (data.request_status.toLowerCase() === "approved") {
                    statusText.classList.add("approved");
                } else if (data.request_status.toLowerCase() === "rejected") {
                    statusText.classList.add("rejected");
                }

                // Show the status box
                statusBox.style.display = 'block';
            } else {
                // Show error message if request details cannot be fetched
                alert("Error fetching request details. Please check the Request ID.");
                statusBox.style.display = 'none'; // Hide status box if there is an error
                statusResult.textContent = "No request found with the provided ID.";
            }
        } catch (error) {
            console.error("Error fetching request details:", error);
            alert("Something went wrong while fetching request details.");
            statusBox.style.display = 'none'; // Hide status box in case of error
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

        // Remove request-id-container from view
        requestIdContainer.style.display = "none";
    });
});
