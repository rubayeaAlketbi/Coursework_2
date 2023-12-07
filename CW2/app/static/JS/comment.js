$(document).ready(function () {
  // Comment submission via AJAX
  $("#commentForm").submit(function (e) {
    // Prevent form submission
    e.preventDefault();
    // Get the post ID
    var commentText = $("#commentText").val();
    var csrfToken = $('input[name="csrf_token"]').val();
    // Send AJAX request
    $.ajax({
      url: "/post/" + post_id,
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ comment: commentText }),
      dataType: "json",
      // Add CSRF token to headers
      headers: {
        "X-CSRFToken": csrfToken,
      },
      // Handle success and error
      success: function (response) {
        console.log("Success: ", response);
      },
      error: function (xhr, status, error) {
        console.error("Error: ", xhr.responseText);
      },
    });
  });
});
