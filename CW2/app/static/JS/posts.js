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



document.addEventListener('DOMContentLoaded', (event) => {

    // Function to sort elements in ascending order
    function sortAscending() {
      let items = document.querySelectorAll('.item'); // Replace with your actual items' class
      items = Array.from(items);
      items.sort((a, b) => a.textContent.localeCompare(b.textContent));
  
      const container = document.querySelector('.items-container'); // Replace with your actual container's class
      items.forEach(item => container.appendChild(item));
    }
  
    // Function to sort elements in descending order
    function sortDescending() {
      let items = document.querySelectorAll('.item'); // Replace with your actual items' class
      items = Array.from(items);
      items.sort((a, b) => b.textContent.localeCompare(a.textContent));
  
      const container = document.querySelector('.items-container'); // Replace with your actual container's class
      items.forEach(item => container.appendChild(item));
    }
  
    // Function to randomize elements
    function randomizeItems() {
      let items = document.querySelectorAll('.item'); // Replace with your actual items' class
      items = Array.from(items);
      for (let i = items.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [items[i], items[j]] = [items[j], items[i]];
      }
  
      const container = document.querySelector('.items-container'); // Replace with your actual container's class
      items.forEach(item => container.appendChild(item));
    }
  
    // Attach events to buttons
    document.querySelector('#SortAsc').addEventListener('click', sortAscending);
    document.querySelector('#SortDesc').addEventListener('click', sortDescending);
    document.querySelector('#Randomize').addEventListener('click', randomizeItems);
  
  });
  