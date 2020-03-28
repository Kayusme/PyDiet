from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients.ingredient_service import IngredientService
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Choose an option:
(s) - Save the ingredient.
(1) - Set ingredient name.
(2) - Set ingredient cost.
(3) - Set ingredient flags.
(4) - Set macronutrient totals.
(5) - Set a macronutrient.
(6) - Set a micronutrient.
'''


class IngredientEditMenuComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('pydiet.ingredient_service')
        self._set_ingredient_name_message:str = 'Ingredient name must be set first.'
        self.set_option_response('1', self.on_set_name)
        self.set_option_response('2', self.on_set_cost)
        self.set_option_response('3', self.on_set_flags)
        self.set_option_response('4', self.on_set_macro_totals)
        self.scope:'IngredientEditService' = inject('pydiet.ingredient_edit_service')

    def run(self):
        self.scope.show_ingredient_summary()

    def print(self):
        output = _TEMPLATE
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def on_set_name(self):
        self.goto('.name')

    def on_set_cost(self):
        self.goto('.cost_mass')

    def on_set_flags(self):   
        # If the ingredient has no name, prompt the user for it first;
        if not self.scope.ingredient.name:
            self.app.error_message = self._set_ingredient_name_message
        # The name is set;
        else:
            # If all flags undefined, ask to cycle;
            if self.scope.ingredient.all_flags_undefined:
                self.goto('.flags.set_all?')
            # Otherwise, just show the flag menu;
            else:
                self.goto('.flags')

    def on_set_macro_totals(self):
        # Set macro totals as the current nutrient category;
        self.scope.current_nutrient_group = 'macro_totals'
        # If the ingredient has no name, prompt the user for it first;
        if not self.scope.ingredient.name:
            self.app.error_message = self._set_ingredient_name_message
        # The name is set;
        else:
            # Navigate to the macro totals menu;
            self.goto('.macro_totals')