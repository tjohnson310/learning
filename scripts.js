// Wait for DOM content to load
document.addEventListener('DOMContentLoaded', function() {

    // Get all elements with class 'nav-link'
    let links = document.querySelectorAll('.nav-link, .nav-link.active');

    // Add event listeners to each hyperlink
    for (let i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function() {

            // Remove 'active' class from all active links
            for (let j = 0; j < links.length; j++) {
                links[j].classList.remove("active");
            }

            // When the hyperlink is clicked, it should be set to 'active'
            links[i].classList.add("active");
        });
    }
});
