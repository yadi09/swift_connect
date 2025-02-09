document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".approve-btn").forEach(button => {
        button.addEventListener("click", (event) => {
            const row = event.target.closest("tr");
            const requestId = row.querySelector("td:nth-child(3)").innerText.trim(); // Get request ID

            // Update status in the UI
            row.querySelector(".status").innerText = "Approved";
            row.querySelector(".status").style.color = "green";

            // Send the request to update the database
            fetch("/update_request", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    request_id: requestId,  // Send correct request ID
                    status: "Approved"
                })
            }).then(response => {
                if (response.ok) {
                    console.log("Request updated successfully");
                } else {
                    console.error("Failed to update request");
                }
            });
        });
    });


    document.querySelectorAll(".reject-btn").forEach(button => {
        button.addEventListener("click", (event) => {
            const row = event.target.closest("tr");
            const requestId = row.querySelector("td:nth-child(3)").innerText.trim(); // Get request ID

            // Update status in the UI
            row.querySelector(".status").innerText = "Rejected";
            row.querySelector(".status").style.color = "red";

            // Send the request to update the database
            fetch("/update_request", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    request_id: requestId,  // Send correct request ID
                    status: "Rejected"
                })
            }).then(response => {
                if (response.ok) {
                    console.log("Request updated successfully");
                } else {
                    console.error("Failed to update request");
                }
            });
        });
    });

    document.querySelector(".logout-btn").addEventListener("click", () => {
        fetch("/logout", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
    });


    const profileBox = document.getElementById("profileBox");
    const profileCompany = document.getElementById("profileCompany");
    const profileRequest = document.getElementById("profileRequest");
    const profileBusiness = document.getElementById("profileBusiness");
    const profileSwift = document.getElementById("profileSwift");
    const profileReason = document.getElementById("profileReason");
    const profileStatus = document.getElementById("profileStatus");

    document.querySelectorAll(".request-row").forEach(row => {
        row.addEventListener("mouseenter", (event) => {
            const data = row.dataset;
            console.log("00000", data);

            profileCompany.innerText = data.company;
            profileRequest.innerText = data.request;
            profileBusiness.innerText = data.business;
            profileSwift.innerText = data.swift;
            profileReason.innerText = data.reason;
            profileStatus.innerText = data.status;
            // Add class to the profileStatus element for dynamic styling based on status value
            profileStatus.classList.remove("approved", "rejected");
            profileStatus.classList.add(data.status.toLowerCase());

            profileBox.style.display = "block";
            profileBox.style.left = event.pageX + 20 + "px";
            profileBox.style.top = event.pageY + "px";
            profileBox.style.transform = "scale(1)";
        });

        row.addEventListener("mousemove", (event) => {
            profileBox.style.left = event.pageX + 20 + "px";
            profileBox.style.top = event.pageY + "px";
        });

        row.addEventListener("mouseleave", () => {
            profileBox.style.display = "none";
        });
    });
});