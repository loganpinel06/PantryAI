//Pantry.js will handle all DOM manipulation for the pantry_table, pantry_form, and generate_recipes_form sections of the pantry.html template
//by using the Fetch API to communicate with the Flask server and update the pantry items dynamically

//create a async function to fetch the pantry items returned from the flask form on the server
const fetchPantryItems = async (event) => {
    //prevent the default form submission behavior
    event.preventDefault();
    //get the table body element from the DOM ,the form element, and the input field from the form
    const tableBody = document.getElementById('pantry-table-body');
    const form = document.getElementById('pantry-form');
    //create a new FormData object to send the ingredient input
    const formData = new FormData(form);
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
        newRow.innerHTML = `
            <td>${pantryData.ingredient}</td>
            <td>
                <button type="button" class="delete-button" data-id="${pantryData.id}">Delete</button>
            </td>
        `;
        //set the newRow's dataset id to the pantry item id
        newRow.dataset.id = pantryData.id;
        //add the new pantry item to the table body
        tableBody.appendChild(newRow);
        //add event listener to the new delete button
        const newDeleteButton = newRow.querySelector('.delete-button');
        newDeleteButton.addEventListener('click', deletePantryItem);
        //reset the value of the input field
        form.reset();
            
    } catch (error) {
        //log the error to the console
        console.error('Error fetching pantry items:', error);
    }
};

//create an async function to delete a pantry item
const deletePantryItem = async (event) => {
    //get the id from the button's data-id attribute
    const itemId = event.target.dataset.id;
    try {
        //fetch the pantry item to delete from the server route
        const response = await fetch(`/api/pantry/delete-ingredient/${itemId}`, {
            method: 'DELETE'
        });
        //check if the response is not ok and throw an error
        if (!response.ok) {
            throw new Error(`Problem deleting pantry item from server route: /api/pantry/delete-ingredient/${itemId}`);
        }
        //parse the response as JSON
        const pantryData = await response.json();
        //get the table body element from the DOM
        const tableBody = document.getElementById('pantry-table-body');
        const rows = tableBody.querySelectorAll('tr');
        //create a boolean variable to help ensure the correct row is found and removed
        let rowFound = false;
        //loop through the rows to find the one with the matching id
        rows.forEach(row => {
            const rowId = row.dataset.id.toString();
            //if the row id matches the pantry item id, remove the row from the table body
            if (rowId === pantryData.id.toString()) {
                rowFound = true; //set the rowFound variable to true
                tableBody.removeChild(row);
            }
        });
        if (!rowFound) { //log an error message if no matching row is found
            console.log(`No matching row found for an ingredient with id: ${pantryData.id}`);
        }
    } catch (error) {
        //log the error to the console
        console.error('Error deleting pantry item:', error);
    }
};

//create an async function to generate recipes based on the pantry items provided
const generateRecipes = async (event) => {
    //prevent the default form submission behavior
    event.preventDefault();
    //get the div element to display the recipes from the DOM
    const recipesDiv = document.getElementsByClassName('recipe_section')[0];
    //get the form element from the DOM
    const form = document.getElementById('generate-recipes-form');
    //create a new FormData object to send the form data
    const formData = new FormData(form);
    //try, catch block to handle errors
    try {
        //fetch the recipes from the server route
        const response = await fetch('/api/gemini/generate-recipes', {
            method: 'POST',
            body: formData
        });
        //check if the response is not ok and throw an error
        if (!response.ok) {
            throw new Error('Problem fetching recipes from server route: /api/gemini/generate-recipes');
        }
        //parse the response as JSON
        const recipesData = await response.json();
        //clear the recipes div
        recipesDiv.innerHTML = '';
        
        //create new divs for each recipe and append them to the recipes div
        recipesData.forEach(recipe => {
            const recipeDiv = document.createElement('div');
            recipeDiv.className = 'recipe-item';
            recipeDiv.innerHTML = `
                <h3>${recipe.recipe_name}</h3>
                <h4>Ingredients:</h4>
                <ul>
                    ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                </ul>
                <h4>Instructions:</h4>
                <p>${recipe.instructions}</p>
            `;
            recipesDiv.appendChild(recipeDiv);
        });

        //reset the form
        form.reset();

    } catch (error) {
        //log the error to the console
        console.error('Error generating recipes:', error);
    }
};

//get the pantry form from the DOM so we can submit it
const pantryForm = document.getElementById('pantry-form');
//add an event listener to the submit button to call the fetchPantryItems function when clicked
pantryForm.addEventListener('submit', fetchPantryItems);

//get the delete buttons from the DOM
const deleteButtons = document.querySelectorAll('.delete-button');
//loop through the delete buttons on the DOM and add an event listener to each one
deleteButtons.forEach(button => {
    button.addEventListener('click', deletePantryItem);
});

//get the generate recipes form from the DOM
const generateRecipesForm = document.getElementById('generate-recipes-form');
//add an event listener to the submit button to call the generateRecipes function when clicked
generateRecipesForm.addEventListener('submit', generateRecipes);