from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''
    ____ of {ingredient_name} costs £__.____
    ^^^^ 

Enter the weight or volume, and units of {ingredient_name}
which you know the cost of.
(e.g 100g, or 1kg, 1L, etc.)
'''


class EditCostMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject(\
            'pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def run(self):
        # Zero the volume temp fields on ies;
        self._ies.temp_volume = None
        self._ies.temp_volume_units = None

    def print(self):
        output = _TEMPLATE.format(\
            ingredient_name=self._ies.ingredient.name)
        output = self.app.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Lowercase the response;
        response = response.lower()
        # Try and parse the response as mass and units;
        try:
            qty_and_units = self._us.parse_number_and_units(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)
            return
        # Grab the units term;
        qty = qty_and_units[0]
        units = qty_and_units[1]
        # Catch volume usage without density definition;
        if units in self._us.recognised_vol_units() and \
            not self._ies.ingredient.density_is_defined:
            self.goto('..edit_density_question')
            return
        # Catch unrecognised unit failure;
        if not units in self._us.recognised_mass_units() and \
            not units in self._us.recognised_vol_units():
            self.app.error_message = "{} is not a recognised unit.".format(units)
            return
        # If we are defining by volume;
        if units in self._us.recognised_vol_units():
            # Stash the volume and units for use in the next template;
            self._ies.temp_volume = qty
            self._ies.temp_volume_units = units
            # Use the density to get the mass in g for the given volume;
            qty = self._ies.ingredient.convert_vol_to_grams(qty, units)
            units = 'g'
        # Stash these values and move on to collect the cost;
        self._ies.temp_cost_mass = qty
        self._ies.temp_cost_mass_units = units
        self.goto('..edit_cost')
