document.addEventListener('DOMContentLoaded', function() {
    const showMoreButton = document.getElementById('show-more-feedback');
    const moreFeedbackSection = document.querySelector('.more-feedback');

    if (showMoreButton) {
        showMoreButton.addEventListener('click', function() {
            moreFeedbackSection.style.display = 'block'; // Show all feedback
            this.style.display = 'none'; // Hide the "Show More" button
        });
    }
    const seeMoreBtn = document.getElementById('see-more-btn');
    const hiddenFeedback = document.querySelectorAll('.hidden');

    if (seeMoreBtn) {
        seeMoreBtn.addEventListener('click', function() {
            hiddenFeedback.forEach(function(item) {
                item.classList.remove('hidden');
            });
            seeMoreBtn.style.display = 'none'; // Hide the button after clicking
        });
    }
});