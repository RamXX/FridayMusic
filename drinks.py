import dspy

from configparser import ConfigParser
from typing import Tuple, Optional, List
from pydantic import BaseModel, StrictStr

from config import Mood
#
# Pydantic classes first
#
class Liquor(BaseModel):
    name: StrictStr
    category: StrictStr  # e.g., "whiskey", "vodka", "gin", "rum", etc.
    brand: Optional[StrictStr] = None
    abv: Optional[float] = None  # Alcohol by volume (percentage)

class AvailableLiquors(BaseModel):
    liquors: List[Liquor]

class Drink(BaseModel):
    name: StrictStr
    ingredients: List[StrictStr]
    instructions: Optional[StrictStr] = None
    garnish: Optional[StrictStr] = None
    glass: Optional[StrictStr] = None
    category: Optional[StrictStr] = None  # e.g., "cocktail", "highball", "shot", etc.

class FavoriteDrinks(BaseModel):
    drinks: List[Drink]

class RecommendDrink(dspy.Signature):
    """Recommend a drink appropriate for the mood based on what the user likes and what's available in the provided list."""
    mood: Mood = dspy.InputField(desc="The user's mood")
    available_liquors: AvailableLiquors = dspy.InputField(desc="List of liquors available to the user. Do not recommend a drink with liquors not in this list.")
    favorite_drinks: FavoriteDrinks = dspy.InputField(desc="The users's favorite drinks. Use this as guidance but feel free to be creative.")
    drink: Drink = dspy.OutputField(desc="Drink recommendation.")

#
# Functions
#
def read_drinks_config(config: ConfigParser) -> Tuple[AvailableLiquors, FavoriteDrinks]:
    """Reads the lists of available liquours and favorite drinks"""
    available_liquors = AvailableLiquors(liquors=[])
    for liquor_info in config.items('AvailableLiquors'):
        liquor_data = liquor_info[1].split(', ')
        name = liquor_data[0]
        category = liquor_data[1] if len(liquor_data) > 1 else ""
        brand = liquor_data[2] if len(liquor_data) > 2 else ""
        abv = float(liquor_data[3]) if len(liquor_data) > 3 else None
        liquor = Liquor(name=name, category=category, brand=brand, abv=abv)
        available_liquors.liquors.append(liquor)

    favorite_drinks = FavoriteDrinks(drinks=[])
    for drink_info in config.items('FavoriteDrinks'):
        drink_data = drink_info[1].split(', ')
        name = drink_data[0]
        ingredients = drink_data[1].split('|') if len(drink_data) > 1 else []
        instructions = drink_data[2] if len(drink_data) > 2 else ""
        garnish = drink_data[3] if len(drink_data) > 3 else ""
        glass = drink_data[4] if len(drink_data) > 4 else ""
        category = drink_data[5] if len(drink_data) > 5 else ""
        drink = Drink(
            name=name,
            ingredients=ingredients,
            instructions=instructions,
            garnish=garnish,
            glass=glass,
            category=category,
        )
        favorite_drinks.drinks.append(drink)

    return available_liquors, favorite_drinks

def recommend_drink(config: ConfigParser, week_mood: Mood) -> Drink:
    """Calls the LM via DSPy to recommend a drink based on the Signature"""
    available_liquors, favorite_drinks = read_drinks_config(config)
    recommender = dspy.TypedChainOfThought(RecommendDrink)
    recommendation = recommender(mood=week_mood, available_liquors=available_liquors, favorite_drinks=favorite_drinks)
    selected_drink: Drink = recommendation.drink
    return selected_drink