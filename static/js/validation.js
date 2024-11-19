function showNext() {
    // Hide Step 1
    document.getElementById('step1').style.display = 'none';
    // Show Step 2
    document.getElementById('step2').style.display = 'block';
}

function showNext2() {
    // Hide Step 2
    document.getElementById('step2').style.display = 'none';
    // Show Step 3
    document.getElementById('step3').style.display = 'block';
}

function showPrevious1() {
    // Hide Step 2
    document.getElementById('step2').style.display = 'none';
    // Show Step 1
    document.getElementById('step1').style.display = 'block';
}

function showPrevious2() {
    // Hide Step 3
    document.getElementById('step3').style.display = 'none';
    // Show Step 2
    document.getElementById('step2').style.display = 'block';
}

function validateForm() {
let isValid = true; // Flag to check if the form is valid
let errorMessages = []; // Array to store error messages

// Get form fields
let username = document.getElementById("id_username").value.trim();
let email = document.getElementById("id_email").value.trim();
let phone = document.getElementById("id_phone").value.trim();
let password1 = document.getElementById("id_password1").value.trim();
let password2 = document.getElementById("id_password2").value.trim();
let genre = document.querySelectorAll("input[name='genre']:checked").length;
let language = document.querySelectorAll("input[name='language']:checked").length;
let securityQuestion = document.getElementById("id_security_question").value;
let securityAnswer = document.getElementById("id_security_answer").value.trim();
let termsChecked = document.getElementById("check").checked;

// Validate username
if (username === "") {
    errorMessages.push("Username is required.");
    isValid = false;
}

// Validate email
if (email === "") {
    errorMessages.push("Email is required.");
    isValid = false;
} else if (!/^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]{2,}(\.[a-zA-Z]{2,})+$/.test(email)) {
    errorMessages.push("Invalid email format.");
    isValid = false;
}

// Validate phone number
if (phone === "") {
    errorMessages.push("Phone number is required.");
    isValid = false;
} else if (!/^\d{10}$/.test(phone)) {
    errorMessages.push("Phone number must be 10 digits.");
    isValid = false;
}

// Validate passwords
if (password1 === "" || password2 === "") {
    errorMessages.push("Both password fields are required.");
    isValid = false;
} else if (password1 !== password2) {
    errorMessages.push("Passwords do not match.");
    isValid = false;
} else if (password1.length < 8) {
    errorMessages.push("Password must be at least 8 characters.");
    isValid = false;
}

// Validate genre
if (genre === 0) {
    errorMessages.push("Please select at least one genre.");
    isValid = false;
}

// Validate language
if (language === 0) {
    errorMessages.push("Please select at least one language.");
    isValid = false;
}

// Validate security question and answer
if (securityQuestion === "") {
    errorMessages.push("Please select a security question.");
    isValid = false;
}

if (securityAnswer === "") {
    errorMessages.push("Security answer is required.");
    isValid = false;
}

// Validate terms and conditions
if (!termsChecked) {
    errorMessages.push("You must accept the terms and conditions.");
    isValid = false;
}

// Show error messages
if (!isValid) {
    alert(errorMessages.join("\n"));
}

return isValid;
}
