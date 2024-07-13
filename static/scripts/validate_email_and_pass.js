async function validateForm() {
    const email = document.getElementById("floatingInput").value;
    const password = document.getElementById("floatingPassword").value;
    const confirm_password = document.getElementById("floatingConfirmPassword").value;

    if (password !== confirm_password) {
        alert("Passwords do not match!");
        return false;
    }
    
    // ChatGPT
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address!");
        return false;
    }

    // ChatGPT
    const email_response = await fetch("/check-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({email: email})
    });

    // ChatGPT
    const data = await email_response.json();
    if (data.exists) {
        alert("Email already registered!");
        return false;
    }

    return true;
}

document.getElementById("signUpForm").addEventListener("submit", async function(event) {
    const isValid = await validateForm();
    if (!isValid) {
        event.preventDefault();
    }
});