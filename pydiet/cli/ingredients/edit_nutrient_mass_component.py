from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients.exceptions import (
    ConstituentsExceedGroupError,
    NutrientQtyExceedsIngredientQtyError
)
from pydiet.shared.exceptions import UnknownUnitError

if TYPE_CHECKING:
    from pydiet.shared import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_NUTRIENT_MASS = '''
    In {qty}{units} of {ingredient_name} there is

    ______ of {nutrient_name}
    ^^^^^^
Enter the weight and units of {nutrient_name}
present in {qty}{units} of {ingredient_name}.
(e.g 100g or 1kg, etc.)
 '''

class EditNutrientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject('pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        # Configure qty and units depending on whether the ingredient
        # cost is being defined per volume or per mass;
        qty = self._ies.temp_nutrient_ingredient_mass
        units = self._ies.temp_nutrient_ingredient_mass_units
        if not self._ies.temp_volume == None and \
            not self._ies.temp_volume_units == None:
            qty = self._ies.temp_volume
            units = self._ies.temp_volume_units        
        output = _NUTRIENT_MASS.format(
            ingredient_name = self._ies.ingredient.name,
            nutrient_name = self._ies.current_nutrient_amount.name,
            qty= qty,
            units = units
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass_and_units = self._us.parse_number_and_units(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)
            return
        # Split the mass and units out;
        mass = mass_and_units[0]
        unit = mass_and_units[1]
        # Try the nutrient data to the ingredient;
        try:
            self._ies.ingredient.set_nutrient_amount(
                self._ies.current_nutrient_amount.name,
                self._ies.temp_nutrient_ingredient_mass,
                self._ies.temp_nutrient_ingredient_mass_units,
                mass, # mass value
                unit # units value
            )
        except (ConstituentsExceedGroupError, NutrientQtyExceedsIngredientQtyError) as err:
            self.app.error_message = (str(err))
            return
        except UnknownUnitError as err:
            self.app.error_message = "{} is not a recognised unit.".format(unit)
            return
        # Navigate back to the nutrient menu;
        self.goto('..')
  