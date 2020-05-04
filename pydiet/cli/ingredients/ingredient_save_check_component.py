from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent
from pydiet.ingredients.exceptions import DuplicateIngredientNameError

if TYPE_CHECKING:
    from pydiet.data import repository_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

class IngredientSaveCheckComponent(YesNoDialogComponent):

    def __init__(self):
        super().__init__()
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self.set_option_response('y', self.on_yes_save)
        self.set_option_response('n', self.on_no_dont_save)
        self.message:str = 'Save changes to this ingredient?'
        self.guarded_route:str

    def on_yes_save(self):
        if not self._ies.ingredient:
            raise ValueError('Ingredient service does not have an active ingredient')
        try:
            # If we have not saved yet;
            if not self._ies.datafile_name:
                # Create new ingredient and populate the datafile name;
                self._ies.datafile_name = self._rp.create_ingredient(self._ies.ingredient)
            # We are saving an edit;
            else:
                # Update the ingredient;
                self._rp.update_ingredient(self._ies.ingredient, self._ies.datafile_name)
        except DuplicateIngredientNameError:
            self.app.error_message = 'There is already an ingredient called {}. Choose another name or edit this ingredient.'\
                .format(self._ies.ingredient.name)
            return None
        except:
            self.app.error_message = 'There was an error saving the ingredient.'
            return None
        self.app.info_message = 'Ingredient saved.'
        self.app.clear_exit(self.guarded_route)      

    def on_no_dont_save(self):
        self.app.info_message = 'Ingredient not saved.'
        self.app.clear_exit(self.guarded_route)     