//saved-recipes.js will handle all DOM manipulation for the saved-recipes.html template

//get the recipe-card div from the DOM
const recipeCard = document.querySelector('.recipe-card');

//get the saved-recipe-button element from the recipe-card
const savedRecipeButton = recipeCard.querySelector('.saved-recipe-button');
//get the recipe-dialog element from the recipe-card
const recipeDialog = recipeCard.querySelector('.recipe-dialog');
//get the close-dialog button element from the recipe-dialog
const closeDialogButton = recipeDialog.querySelector('.close-dialog');
//get the delete-saved-recipe button element from the recipe-dialog
const deleteSavedRecipeButton = recipeDialog.querySelector('.delete-saved-recipe');

//create event listeners for the buttons
//savedRecipeButton (show dialog modal)
savedRecipeButton.addEventListener('click', () => {
    //open the dialog when the saved recipe button is clicked
    recipeDialog.showModal();
});
//closeDialogButton (close dialog modal)
closeDialogButton.addEventListener('click', () => {
    //close the dialog when the close button is clicked
    recipeDialog.close();
});
//deleteSavedRecipeButton (delete saved recipe by calling api route)
