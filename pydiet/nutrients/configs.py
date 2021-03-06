from typing import List, Dict

all_primary_nutrient_names: List[str] = [
    "a_carotene",
    "a_linolenic_acid",
    "alanine",
    "alcohol",
    "amylopectin",
    "amylose",
    "arachidic_acid",
    "arachidonic_acid",
    "arginine",
    "asparagine",
    "aspartic_acid",
    "b_carotene",
    "behenic_acid",
    "biotin",
    "butyric_acid",
    "calcium",
    "capric_acid",
    "caproic_acid",
    "caprylic_acid",
    "carbohydrate",
    "cartenoids",
    "cerotic_acid",
    "cervonic_acid",
    "chloride",
    "cholecalciferol",
    "choline",
    "chromium",
    "clupanodonic_acid",
    "cobalamin",
    "copper",
    "cryptoxanthin",
    "cysteine",
    "eicosen",
    "ergocalciferol",
    "erucic_acid",
    "fat",
    "fibre",
    "folate",
    "fructose",
    "galactose",
    "glucose",
    "glutamic_acid",
    "glutamine",
    "glycine",
    "heptadecenoic",
    "histidine",
    "iodine",
    "iron",
    "isoleucine",
    "lactose",
    "lauric_acid",
    "leucine",
    "lignoceric_acid",
    "linoleic_acid",
    "lutein",
    "lycopene",
    "lysine",
    "magnesium",
    "maltose",
    "manganese",
    "margaric_acid",
    "methionine",
    "molybdenum",
    "monounsaturated_fat",
    "myristic_acid",
    "myristol",
    "nervonic_acid",
    "niacin",
    "oleic_acid",
    "omega_3",
    "omega_6",
    "palmitic_acid",
    "palmitoyl",
    "pantothenic_acid",
    "pentadecanoic_acid",
    "pentadecenoic",
    "phenylalanine",
    "phosphorus",
    "polyunsaturated_fat",
    "potassium",
    "proline",
    "protein",
    "pyridoxal_5_phosphate",
    "pyridoxamine",
    "pyridoxine",
    "retinal",
    "retinoic_acid",
    "retinol",
    "riboflavin",
    "ribose",
    "saturated_fat",
    "selenium",
    "serine",
    "sodium",
    "stearic_acid",
    "stearidonic_acid",
    "sucrose",
    "thiamin",
    "threonine",
    "timnodonic_acid",
    "trans_fats",
    "tryptophan",
    "tyrosine",
    "valine",
    "vitamin_a",
    "vitamin_b6",
    "vitamin_c",
    "vitamin_d",
    "vitamin_d2",
    "vitamin_d3",
    "vitamin_e",
    "vitamin_k",
    "vitamin_k1",
    "vitamin_k2",
    "zeaxanthin",
    "zinc"
]

mandatory_nutrient_names: List[str] = [
    "carbohydrate",
    "fat",
    "saturated_fat",
    "monounsaturated_fat",
    "polyunsaturated_fat",
    "protein",
    "sodium"
]

nutrient_aliases: Dict[str, List[str]] = {
    "a_carotene": ["alpha_carotene"],
    "a_linolenic_acid": ["alpha_linolenic_acid", "ALA"],
    "amylose": ["starch"],
    "arachidic_acid": ["C20"],
    "arachidonic_acid": ["ETA"],
    "aspartic_acid": ["aspartate"],
    "b_carotene": ["beta_carotene"],
    "behenic_acid": ["C22", "docosanoic_acid"],
    "biotin": ["vitamin_b7"],
    "butyric_acid": ["C4"],
    "capric_acid": ["C10"],
    "caproic_acid": ["C6"],
    "caprylic_acid": ["C8"],
    "cerotic_acid": ["C26"],
    "cervonic_acid": ["DHA"],
    "clupanodonic_acid": ["DPA"],
    "cobalamin": ["vitamin_b12"],
    "folate": ["vitamin_b9"],
    "glutamic_acid": ["glutamate"],
    "lauric_acid": ["C12"],
    "lignoceric_acid": ["C24"],
    "linoleic_acid": ["LA"],
    "margaric_acid": ["C17"],
    "myristic_acid": ["C14"],
    "niacin": ["vitamin_b3"],
    "palmitic_acid": ["C16"],
    "pantothenic_acid": ["vitamin_b5"],
    "pentadecanoic_acid": ["C15"],
    "riboflavin": ["vitamin_b2"],
    "stearic_acid": ["C18"],
    "stearidonic_acid": ["SDA"],
    "thiamin": ["vitamin_b1"],
    "timnodonic_acid": ["EPA", "eicosapentaenoic_acid"],
    "vitamin_c": ["ascorbic_acid"],
    "vitamin_k1": ["phylloquinone"],
    "vitamin_k2": ["menaquinone"],
}

nutrient_group_definitions: Dict[str, List[str]] = {
    "carbohydrate": ["glucose", "sucrose", "ribose", "amylose", "amylopectin", "maltose", "galactose", "fructose",
                     "lactose"],
    "cartenoids": ["a_carotene", "b_carotene", "cryptoxanthin", "lutein", "lycopene", "zeaxanthin"],
    "fat": ["monounsaturated_fat", "polyunsaturated_fat", "saturated_fat", "trans_fats"],
    "fibre": [],
    "monounsaturated_fat": ["myristol", "pentadecenoic", "palmitoyl", "heptadecenoic", "oleic_acid", "eicosen",
                            "erucic_acid", "nervonic_acid"],
    "omega_3": [],
    "omega_6": [],
    "polyunsaturated_fat": [],
    "protein": ["alanine", "arginine", "aspartic_acid", "asparagine", "cysteine", "glutamic_acid", "glutamine",
                "glycine", "histidine", "isoleucine", "leucine", "lysine", "methionine", "phenylalanine", "proline",
                "serine", "threonine", "tryptophan", "tyrosine", "valine"],
    "saturated_fat": [],
    "trans_fats": [],
    "vitamin_a": ["retinol", "retinal", "retinoic_acid", "b_carotene"],
    "vitamin_b6": ["pyridoxine", "pyridoxal_5_phosphate", "pyridoxamine"],
    "vitamin_d": ["ergocalciferol", "cholecalciferol"],
    "vitamin_e": [],
    "vitamin_k": ["vitamin_k1", "vitamin_k2"],
}
nutrient_flag_rels: Dict[str, List[str]] = {
    "alcohol_free": ["alcohol"]
}

calorie_nutrients: Dict[str, float] = {
    "protein": 4,
    "fat": 9,
    "carbohydrate": 4,
    "alcohol": 7
}