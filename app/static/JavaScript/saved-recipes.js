//saved-recipes.js will handle all DOM manipulation for the saved-recipes.html template

//get all the recipe-card divs from the DOM
const recipeCards = document.querySelectorAll('.recipe-card');

//loop through all recipe cards and add event listeners to each one allowing access to the dialog modal
recipeCards.forEach(recipeCard => {
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
        //ensure the dialog scrolls to the top
        recipeDialog.scrollTop = 0;
    });
    //closeDialogButton (close dialog modal)
    closeDialogButton.addEventListener('click', () => {
        //close the dialog when the close button is clicked
        recipeDialog.close();
    });
    //deleteSavedRecipeButton (delete saved recipe by calling api route)
    deleteSavedRecipeButton.addEventListener('click', async () => {
        //try, catch block to handle errors
        try {
            //fetch the delete saved recipe route on the server which will trigger the deletion of the recipe from the database
            const response = await fetch(`/api/gemini/delete-recipe/${deleteSavedRecipeButton.dataset.recipeId}`, {
                method: 'DELETE'
            });
            //check if the response is not ok and throw an error
            if (!response.ok) {
                throw new Error('Error fetching saved recipe to delete from server route: /api/gemini/delete-recipe');
            }
            //parse the response as JSON (best practice even if we don't use it)
            const result = await response.json();

            //now clean up the DOM by removing the parent recipe-card element of the delete button and closing the dialog modal
            //get the recipe card we need to delete (closest parent to the deleteSavedRecipeButton with class recipe-card)
            const recipeCardToDelete = deleteSavedRecipeButton.closest('.recipe-card');
            //get the dialog modal to close it (closest parent to the deleteSavedRecipeButton with class recipe-dialog)
            const dialogToClose = deleteSavedRecipeButton.closest('.recipe-dialog');
            //close the dialog modal
            dialogToClose.close();
            //remove the recipe card from the DOM
            recipeCardToDelete.remove();
        //catch any errors
        } catch (error) {
            console.error("Error deleting saved recipe:",error);
        }
    });
});