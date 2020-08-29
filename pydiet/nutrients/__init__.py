from typing import Dict

from pydiet.nutrients import (configs,
                              exceptions,
                              nutrient,
                              supports_nutritional_composition,
                              supports_nutrient_quantities,
                              supports_nutrient_targets,
                              nutrients_service)

# Init the global nutrient instances;
global_nutrients:Dict[str, nutrient.Nutrient] = {}

for nutrient_name in configs.all_primary_nutrient_names:
    if not nutrient_name in global_nutrients.keys():
        global_nutrients[nutrient_name] = nutrient.Nutrient(nutrient_name)