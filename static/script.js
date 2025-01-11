// script.js
document.addEventListener("DOMContentLoaded", function() {
    // Confirm delete action
    const deleteForms = document.querySelectorAll("form[action*='/delete/']");
    deleteForms.forEach(form => {
        form.addEventListener("submit", function(e) {
            const confirmed = confirm("Are you sure you want to delete this annotation?");
            if (!confirmed) {
                e.preventDefault();  // Prevent form submission if not confirmed
            }
        });
    });
});
