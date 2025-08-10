//Pantry.js will handle all DOM manipulation for the pantry_table, pantry_form, and generate_recipes_form sections of the pantry.html template
//by using the Fetch API to communicate with the Flask server and update the pantry items dynamically

//BASIC FUNCTIONS (Not API related)
//function to check if the pantry is empty and display/hide a message telling users to add ingredients
const checkPantryEmpty = () => {
    //get the table body and any existing empty pantry messages from the DOM
    const tableBody = document.getElementById('pantry-table-body');
    //this should be null if there are pantry items, and an element if there are none
    const existingMessage = document.getElementById('empty-pantry-message');
    
    //create a boolean variable to check if there are any rows in the table body
    const hasItems = tableBody.querySelectorAll('tr').length > 0;
    
    //conditional logic
    if (!hasItems) {
        //if no items and no message exists, create and show the empty message
        if (!existingMessage) {
            //create a new tr element for the message
            const emptyMessage = document.createElement('tr');
            emptyMessage.id = 'empty-pantry-message';
            emptyMessage.innerHTML = `
                <td colspan="2">Pantry Empty! Add Ingredients!</td>
            `;
            //add the element to the tableBody
            tableBody.appendChild(emptyMessage);
        }
    } else {
        // If items exist and message is showing, remove the message
        if (existingMessage) {
            existingMessage.remove();
        }
    }
};

//API FUNCTIONS using Fetch API
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
                <button type="button" class="delete-button" data-id="${pantryData.id}">&times;</button>
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
        //check if the pantry is empty or not
        checkPantryEmpty();
    //catch any errors
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
        //check if the pantry is empty or not
        checkPantryEmpty();
    //catch any errors
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
            //create a new div for the recipe button and dialog
            const recipeButtonDiv = document.createElement('div');
            //set the class name and inner HTML for the recipe button and dialog
            recipeButtonDiv.className = 'recipe-button-div';
            recipeButtonDiv.innerHTML = `
                <button class="recipe-button">${recipe.recipe_name}</button>
                <dialog class="recipe-dialog">
                    <h3>${recipe.recipe_name}</h3>
                    <h4>Meal Type: ${recipe.meal_type}</h4>
                    <h4>Ingredients:</h4>
                    <ul>
                        ${recipe.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
                    </ul>
                    <h4>Instructions:</h4>
                    <ol>
                        ${recipe.instructions.map(instruction => `<li>${instruction}</li>`).join('')}
                    </ol>
                    <button class="close-dialog">Close</button>
                    <button class="save-recipe">Save Recipe</button>
                </dialog>
            `;
            //add event listeners to the recipe and close buttons
            //get the HTML elements
            const recipeButton = recipeButtonDiv.querySelector('.recipe-button');
            const recipeDialog = recipeButtonDiv.querySelector('.recipe-dialog');
            const closeDialogButton = recipeButtonDiv.querySelector('.close-dialog');
            const saveRecipeButton = recipeButtonDiv.querySelector('.save-recipe');
            //handle the events
            recipeButton.addEventListener('click', () => {
                //open the dialog when the recipe button is clicked
                recipeDialog.showModal();
            });
            closeDialogButton.addEventListener('click', () => {
                //close the dialog when the close button is clicked
                recipeDialog.close();
            });
            saveRecipeButton.addEventListener('click', () => saveRecipe(recipe));
            //append the recipe button div to the recipes div
            recipesDiv.appendChild(recipeButtonDiv);
        });

        //reset the form
        form.reset();
    //catch any errors
    } catch (error) {
        //log the error to the console
        console.error('Error generating recipes:', error);
    }
};

//create an async function to handle saving a recipe
const saveRecipe = async (recipe) => {
    //try, catch block to handle errors
    try {
        //fetch the save recipe route on the server
        const response = await fetch('/api/gemini/save-recipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                recipe: recipe.recipe_name,
                meal_type: recipe.meal_type,
                ingredients: recipe.ingredients,
                instructions: recipe.instructions,
            }),
        });
        //check if the response is not ok and throw an error
        if (!response.ok) {
            throw new Error('Problem saving recipe to server route: /api/gemini/save-recipe');
        }
        //parse the response as JSON (best practice even if we don't use it)
        const savedRecipe = await response.json();
    //catch any errors
    } catch (error) {
        //log the error to the console
        console.error('Error saving recipe:', error);
    }
};

//MAIN CODE WHEN DOCUMENT LOADS
//check initial pantry state on page load
checkPantryEmpty();

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