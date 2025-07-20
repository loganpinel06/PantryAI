//create a async function to fetch the pantry items returned from the flask form on the server
const fetchPantryItems = async (event) => {
    //prevent the default form submission behavior
    event.preventDefault();
    //get the table body element from the DOM ,the form element, and the input field from the form
    const tableBody = document.getElementById('pantry-table-body');
    const form = document.getElementById('pantry-form');
    const ingredientInput = document.getElementById('ingredient-input');
    //create a new FormData object to send the ingredient input
    const formData = new FormData(form);
    formData.append('ingredient', ingredientInput.value);
    try {
        //fetch the pantry items from the server
        const response = await fetch('/api/pantry/add-ingredient', {
            method: 'POST',
            body: formData
        });
        //check if the response if not ok and throw an error
        if (!response.ok) {
            throw new Error('Problem fetching pantry items from server route: /api/pantry/add-ingredient');
        }
        //parse the response as JSON
        const pantryData = await response.json();
        //create a new table row on the dom
        const newRow = document.createElement('tr');
        //update the newRow's innerHTML with the pantry data
        newRow.innerHTML = `<td>${pantryData.ingredient}</td>`;
        //add the new pantry item to the table body
        tableBody.appendChild(newRow);
            
    } catch (error) {
        //log the error to the console
        console.error('Error fetching pantry items:', error);
    }
};

//get the submit button from the pantry form on the DOM
const submitButton = document.getElementById('submit-ingredient');
//add an event listener to the submit button to call the fetchPantryItems function when clicked
submitButton.addEventListener('click', fetchPantryItems);