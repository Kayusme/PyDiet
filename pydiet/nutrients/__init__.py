from typing import Dict

from pydiet.nutrients import (configs,
                              exceptions,
                              validation,
                              nutrient,
                              supports_nutrient_content,
                              supports_nutrient_targets,
                              nutrients_service,
                              cli_components)

# Init the global nutrient instances;
global_nutrients: Dict[str, nutrient.Nutrient] = {}

for nutrient_name in configs.all_primary_nutrient_names:
    if nutrient_name not in global_nutrients.keys():
        global_nutrients[nutrient_name] = nutrient.Nutrient(nutrient_name)
