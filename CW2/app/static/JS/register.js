// Used to validate the register form
document.addEventListener("DOMContentLoaded", function () {
  // Add event listener to form
  var registerForm = document.getElementById("registerForm");
  registerForm.addEventListener("submit", function (event) {
    // Prevent form submission
    event.preventDefault();
    // Validate each field
    var isValid = true;
    // get the values from the form
    var username = document.getElementById("username");
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var confirm = document.getElementById("confirm");
    // Check if username is not empty
    if (username.value.trim() === "") {
      isValid = false;
      document.getElementById("usernameError").textContent =
        "Username is required.";
      username.classList.add("is-invalid");
    } else {
      username.classList.remove("is-invalid");
    }
    // Check if email is not empty
    if (email.value.trim() === "") {
      isValid = false;
      document.getElementById("emailError").textContent = "Email is required.";
      username.classList.add("is-invalid");
    } else {
      username.classList.remove("is-invalid");
    }
    // Check if password fields match
    if (password.value !== confirm.value) {
      isValid = false;
      document.getElementById("confirmError").textContent =
        "Passwords do not match.";
      confirm.classList.add("is-invalid");
    } else {
      confirm.classList.remove("is-invalid");
    }
    // Submit form if all fields are valid
    if (isValid) {
      registerForm.submit();
    }
  });
});
