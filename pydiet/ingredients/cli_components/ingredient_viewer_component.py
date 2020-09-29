from typing import Dict

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, StandardPageComponent, menu_tools, ResponseValidationError
from pydiet import persistence, ingredients

_main_view_component = '''
Edit Ingredient | -edit [ingredient number]

Ingredients:
{ingredient_menu}
'''


class IngredientViewerComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._ingredient_num_map: Dict[int, str] = {}

        self.configure_state('main', self._print_main_view, responders=[
            self.configure_responder(self._on_edit_ingredient, args=[
                PrimaryArg('ingr_num', has_value=True, markers=['-edit'], validators=[
                    self._validate_ingredient_number])
            ])
        ])

    @property
    def _ingredient_menu(self) -> str:
        menu = ''
        for num in self._ingredient_num_map:
            menu = menu + '{num}. {ingr_name}\n'.format(
                num=num, ingr_name=self._ingr_name_from_num(num)
            )
        return menu

    def _ingr_name_from_num(self, num: int) -> str:
        return self._ingredient_num_map[num]

    def _validate_ingredient_number(self, value) -> int:
        try:
            num = int(value)
        except ValueError:
            raise ResponseValidationError('Please enter a valid ingredient number.')
        if num not in self._ingredient_num_map:
            raise ResponseValidationError('Please enter a valid ingredient number.')
        return num

    def _before_print(self) -> None:
        ingr_names = persistence.persistence_service.get_saved_unique_vals(ingredients.ingredient.Ingredient)
        self._ingredient_num_map = menu_tools.create_number_name_map(ingr_names)

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print(
            page_title='Ingredient Viewer',
            page_content=_main_view_component.format(
                ingredient_list=self._ingredient_menu
            )
        )

    def _on_edit_ingredient(self, args) -> None:
        iec = self.app.get_component(ingredients.cli_components.ingredient_editor_component.IngredientEditorComponent)
        ingr_name = self._ingr_name_from_num(args['ingr_num'])
        i = persistence.persistence_service.load(ingredients.ingredient.Ingredient, ingr_name)
        iec.configure(ingredient=i)
        self.app.goto('home.ingredients.edit')
