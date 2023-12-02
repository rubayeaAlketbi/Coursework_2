
$(document).ready(function() {
    var csrf_token = $('input[name="csrf_token"]').val();

    $('#username').on('keyup', function() {
        var username = $(this).val().trim();
        if (username.length > 0) {
            $.ajax({
                url: '/register/validate-username',
                type: 'POST',
                data: {
                    username: username,
                    csrf_token: csrf_token
                },
                dataType: 'json',
                success: function(response) {
                    // If the server response indicates success, the username is available
                    if(response.success) {
                        $('#usernameError').text(''); // Clear any existing error messages
                        $('#username').css('border', '1px solid green'); // Optional: change border to green
                        // ... any additional success indicators ...
                    } else {
                        // If the username is not available, use the error message from the server
                        $('#usernameError').text(response.error);
                        $('#username').css('border', '1px solid red'); // Optional: change border to red
                        // ... any additional error indicators ...
                    }
                },
                error: function(xhr, status, error) {
                    // Handle the error if the AJAX call itself fails (e.g., server is down, etc.)
                    $('#usernameError').text('An error occurred while validating the username.');
                    // ... handle other aspects of the error state ...
                }
            });
        } else {
            // If the input is empty, prompt the user to enter a username
            $('#usernameError').text('Username is required.');
            $('#username').css('border', ''); // Reset the border or other styles if necessary
        }
    });
});

