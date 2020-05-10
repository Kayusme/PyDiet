from typing import Dict, TYPE_CHECKING
import json
import uuid
import os

from pinjector import inject

from pydiet.ingredients.exceptions import (
    DuplicateIngredientNameError,
    IngredientNameUndefinedError
)
from pydiet.recipes.exceptions import (
    DuplicateRecipeNameError,
    RecipeNameUndefinedError
)

if TYPE_CHECKING:
    from pydiet.shared import configs


def create_ingredient_data(ingredient_data: Dict) -> str:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Check the ingredient name is populated;
    if not ingredient_data['name']:
        raise IngredientNameUndefinedError
    # Check the ingredient name does not exist already;
    index = read_ingredient_index()
    if ingredient_data['name'] in index.values():
        raise DuplicateIngredientNameError(
            'There is already an ingredient called {}'.format(ingredient_data['name']))
    # Create filename;
    filename = str(uuid.uuid4())
    filename_w_ext = filename+'.json'
    # Update index with filename;
    index[filename] = ingredient_data['name']
    update_ingredient_index(index)
    # Write the ingredient datafile;
    with open(cf.INGREDIENT_DB_PATH+filename_w_ext, 'w') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)
    # Return the datafile name;
    return filename


def create_recipe_data(recipe_data: Dict) -> str:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Check the recipe name is populated;
    if not recipe_data['name']:
        raise RecipeNameUndefinedError
    # Check the recipe name does not exist already;
    index = read_recipe_index()
    if recipe_data['name'] in index.values():
        raise DuplicateRecipeNameError(
            'There is already an recipe called {}'.format(recipe_data['name']))
    # Create filename;
    filename = str(uuid.uuid4())
    filename_w_ext = filename+'.json'
    # Update index with filename;
    index[filename] = recipe_data['name']
    update_recipe_index(index)
    # Write the recipe datafile;
    with open(cf.RECIPE_DB_PATH+filename_w_ext, 'w') as fh:
        json.dump(recipe_data, fh, indent=2, sort_keys=True)
    # Return the datafile name;
    return filename


def read_ingredient_template_data() -> Dict:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    #
    return read_ingredient_data(
        cf.INGREDIENT_DATAFILE_TEMPLATE_NAME)

def read_recipe_template_data() -> Dict:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    #
    return read_recipe_data(
        cf.RECIPE_DATAFILE_TEMPLATE_NAME)

def read_ingredient_data(ingredient_datafile_name: str) -> Dict:
    '''Returns an ingredient datafile as a dict.

    Args:
        ingredient_datafile_name (str): Filename of ingredient
            datafile, without the extension.

    Returns:
        Dict: Ingredient datafile in dictionary format.
    '''
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Read the datafile contents;
    with open(cf.INGREDIENT_DB_PATH+'{}.json'.format(
            ingredient_datafile_name), 'r') as fh:
        raw_data = fh.read()
        # Parse into dict;
        data = json.loads(raw_data)
        # Return it;
        return data

def read_recipe_data(recipe_datafile_name: str) -> Dict:
    '''Returns an recipe datafile as a dict.

    Args:
        recipe_datafile_name (str): Filename of recipe
            datafile, without the extension.

    Returns:
        Dict: recipe datafile in dictionary format.
    '''
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Read the datafile contents;
    with open(cf.RECIPE_DB_PATH+'{}.json'.format(
            recipe_datafile_name), 'r') as fh:
        raw_data = fh.read()
        # Parse into dict;
        data = json.loads(raw_data)
        # Return it;
        return data

def read_ingredient_index() -> Dict[str, str]:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    #
    with open(cf.INGREDIENT_DB_PATH+'{}.json'.
              format(cf.INGREDIENT_INDEX_NAME)) as fh:
        raw_data = fh.read()
        data = json.loads(raw_data)
        return data

def read_recipe_index() ->Dict[str, str]:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    #
    with open(cf.RECIPE_DB_PATH+'{}.json'.
              format(cf.RECIPE_INDEX_NAME)) as fh:
        raw_data = fh.read()
        data = json.loads(raw_data)
        return data    

def update_ingredient_data(ingredient_data: Dict, datafile_name: str) -> None:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Load the index to do some checks;
    index = read_ingredient_index()
    # Check the ingredient name is populated;
    if not ingredient_data['name']:
        raise IngredientNameUndefinedError
    # Check the ingredient name is not used by another datafile;
    # Pop the current name, because if it hasn't changed, we don't want to
    # detect it;
    index.pop(datafile_name)
    # Now current has been removed, check everwhere else for name;
    if ingredient_data['name'] in index.values():
        raise DuplicateIngredientNameError(
            'Another ingredient already uses the name {}'.format(ingredient_data['name']))
    # Write the ingredient data;
    with open(cf.INGREDIENT_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)
    # Update the index;
    index[datafile_name] = ingredient_data['name']
    update_ingredient_index(index)

def update_recipe_data(recipe_data: Dict, datafile_name: str) -> None:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Load the index to do some checks;
    index = read_recipe_index()
    # Check the recipe name is populated;
    if not recipe_data['name']:
        raise RecipeNameUndefinedError
    # Check the recipe name is not used by another datafile;
    # Pop the current name, because if it hasn't changed, we don't want to
    # detect it;
    index.pop(datafile_name)
    # Now current has been removed, check everwhere else for name;
    if recipe_data['name'] in index.values():
        raise DuplicateRecipeNameError(
            'Another recipe already uses the name {}'.format(recipe_data['name']))
    # Write the recipe data;
    with open(cf.RECIPE_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(recipe_data, fh, indent=2, sort_keys=True)
    # Update the index;
    index[datafile_name] = recipe_data['name']
    update_recipe_index(index)

def update_ingredient_index(index: Dict[str, str]) -> None:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    #
    with open(cf.INGREDIENT_DB_PATH+'{}.json'.
              format(cf.INGREDIENT_INDEX_NAME), 'w') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)

def update_recipe_index(index: Dict[str, str]) -> None:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    #
    with open(cf.RECIPE_DB_PATH+'{}.json'.
              format(cf.RECIPE_INDEX_NAME), 'w') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)        


def delete_ingredient_data(datafile_name: str) -> None:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Open the index;
    index = read_ingredient_index()
    # Remove the entry from the index;
    index.pop(datafile_name)
    # Rewrite the index;
    update_ingredient_index(index)
    # Delete the datafile;
    os.remove(cf.INGREDIENT_DB_PATH+datafile_name+'.json')

def delete_recipe_data(datafile_name: str) -> None:
    # Import dependencies;
    cf: 'configs' = inject('pydiet.configs')
    # Open the index;
    index = read_recipe_index()
    # Remove the entry from the index;
    index.pop(datafile_name)
    # Rewrite the index;
    update_recipe_index(index)
    # Delete the datafile;
    os.remove(cf.RECIPE_DB_PATH+datafile_name+'.json')    
