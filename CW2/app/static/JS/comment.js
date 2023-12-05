$(document).ready(function() {
    // Comment submission via AJAX
    $('#commentForm').submit(function(e) {
        // Prevent form submission
        e.preventDefault(); 

        var commentText = $('#commentText').val();
        var csrfToken = $('input[name="csrf_token"]').val();

        $.ajax({
            url: '/post/' + post_id, 
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ comment: commentText }),
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken 
            },
            success: function(response) {
                console.log("Success: ", response);

            },
            error: function(xhr, status, error) {
                console.error("Error: ", xhr.responseText);
            }
        });
    });
});
