document.addEventListener('DOMContentLoaded', function () {
    var registerForm = document.getElementById('registerForm');

    registerForm.addEventListener('submit', function (event) {
        // Prevent form submission
        event.preventDefault();

        // Validate each field
        var isValid = true;

        var username = document.getElementById('username');
        var email = document.getElementById('email');
        var password = document.getElementById('password');
        var confirm = document.getElementById('confirm');

        // Example: Check if username is not empty
        if (username.value.trim() === '') {
            isValid = false;
            document.getElementById('usernameError').textContent = 'Username is required.';
            username.classList.add('is-invalid');
        } else {
            username.classList.remove('is-invalid');
        }

        // Add similar checks for email, password, confirm

        // Check if email is valid
        if (!email.checkValidity()) {
            isValid = false;
            document.getElementById('emailError').textContent = 'Please enter a valid email.';
            email.classList.add('is-invalid');
        } else {
            email.classList.remove('is-invalid');
        }

        // Example: Check if password fields match
        if (password.value !== confirm.value) {
            isValid = false;
            document.getElementById('confirmError').textContent = 'Passwords do not match.';
            confirm.classList.add('is-invalid');
        } else {
            confirm.classList.remove('is-invalid');
        }

        // Submit form if all fields are valid
        if (isValid) {
            registerForm.submit();
        }
    });
});

