$(document).ready(function() {
    $('#commentForm').submit(function(e) {
        e.preventDefault(); // Prevent the default form submission

        var commentText = $('#commentText').val();
        var csrfToken = $('input[name="csrf_token"]').val(); // Fetch the CSRF token

        $.ajax({
            url: '/post/' + post_id, // Ensure this is the correct endpoint
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ comment: commentText }),
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken // Include the CSRF token in the request headers
            },
            success: function(response) {
                console.log("Success: ", response);
                // Add the new comment to the comments section
            },
            error: function(xhr, status, error) {
                console.error("Error: ", xhr.responseText);
            }
        });
    });
});
