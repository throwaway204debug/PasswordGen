
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("generate-btn").addEventListener("click", function() {
        const passwordLength = document.getElementById("password-length").value;

        if (passwordLength < 8 || passwordLength > 100) {
            alert("Password length must be between 8 and 100 characters!");
            return;
        }

        fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ length: passwordLength })
        })
        .then(response => response.json())
        .then(data => {
            const passwordOutput = document.getElementById("password-output");
            if (data.password) {
                passwordOutput.textContent = "Generated Password: " + data.password;
            } else {
                passwordOutput.textContent = "Error: " + (data.error || "Something went wrong.");
            }
        })
        .catch(error => {
            console.error("Error generating password:", error);
        });
    });
});
