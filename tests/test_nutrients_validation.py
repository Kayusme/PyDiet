from unittest import TestCase

from pydiet import nutrients, quantity


class TestValidateNutrientsData(TestCase):

    def setUp(self) -> None:
        self.nd = nutrients.supports_nutrient_content.get_empty_nutrients_data()

    def test_catches_nutrient_name_error(self):
        self.nd['madeup'] = nutrients.supports_nutrient_content.NutrientData(nutrient_g_per_subject_g=0.5,
                                                                             nutrient_pref_units='g')
        with self.assertRaises(nutrients.exceptions.NutrientNameError):
            nutrients.validation.validate_nutrients_data(self.nd)

    def test_catches_nutrient_qty_exceeds_parent_qty(self):
        self.nd['carbohydrate']['nutrient_g_per_subject_g'] = 1.2
        with self.assertRaises(nutrients.exceptions.NutrientQtyExceedsIngredientQtyError):
            nutrients.validation.validate_nutrients_data(self.nd)

    def test_catches_nutrient_qty_units_not_mass(self):
        self.nd['carbohydrate']['nutrient_pref_units'] = 'ml'
        with self.assertRaises(quantity.exceptions.IncorrectUnitTypeError):
            nutrients.validation.validate_nutrients_data(self.nd)

    def test_catches_child_nutrients_exceed_parent_mass(self):
        self.nd['carbohydrate']['nutrient_g_per_subject_g'] = 0.8
        self.nd['glucose']['nutrient_g_per_subject_g'] = 0.5
        self.nd['fructose']['nutrient_g_per_subject_g'] = 0.4
        with self.assertRaises(nutrients.exceptions.ChildNutrientQtyExceedsParentNutrientQtyError):
            nutrients.validation.validate_nutrients_data(self.nd)
