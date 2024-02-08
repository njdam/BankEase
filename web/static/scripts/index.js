// Slide shows on landing page
var slideIndex = 0;

function showSlides() {
    var slides = document.getElementsByClassName("mySlides");

    // Hide all slides
    for (var i = 0; i < slides.length; i++) {
        slides[i].classList.remove("show"); // Remove the "show" class
    }

    // Increment slide index
    slideIndex++;

    // Reset slide index if it exceeds the total number of slides
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    // Display the current slide
    slides[slideIndex - 1].classList.add("show"); // Add the "show" class

    // Schedule the next slide after 2000 milliseconds (2 seconds)
    setTimeout(showSlides, 2000);
}

// Run the slideshow when the page loads
showSlides();
