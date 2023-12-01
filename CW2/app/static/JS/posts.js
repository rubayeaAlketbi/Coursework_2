/**
 * A function that randomize the order of the posts on the explore page
 * it uses the DOMContentLoaded event to trigger the function whenever the page is loaded
 * @param {event} event - The event that triggers the function
 * @returns {void} - Returns nothing
 */
document.addEventListener('DOMContentLoaded', (event) => {
    const container = document.querySelector('.row.d-flex');
    for (let i = container.children.length; i >= 0; i--) {
        container.appendChild(container.children[Math.random() * i | 0]);
    }
});

