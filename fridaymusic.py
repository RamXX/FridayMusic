import dspy
import traceback

from rich.console import Console
from rich import print
from rich.traceback import install as install_traceback
from dotenv import load_dotenv
from configparser import ConfigParser

from config import mood_music
from roon_integration import play_music
from drinks import recommend_drink
from obsidian import process_obsidian_notes

if __name__ == "__main__":
    
    console = Console(record=True)
    _ = install_traceback(console=console, show_locals=True)
    traceback.print_exc()

    if not load_dotenv():
        raise ValueError("Could not load .env file")

    config = ConfigParser()
    config.read('config.ini')

    # You need to make sure you have OPENAI_API_KEY defined in your .env file.
    # Feel free to experiment with other LMs. GPT 3.5 seems perfectly fine for this task.
    lm = dspy.OpenAI(model="gpt-3.5-turbo", max_tokens=512, temperature=0.7)
    dspy.settings.configure(lm=lm)

    week_mood = process_obsidian_notes(f"{config.get('Obsidian', 'vault')}/{config.get('Obsidian', 'daily_notes_folder')}")

    print(f"The mood for the entire week is: [yellow]{week_mood.name.lower().capitalize()}[/yellow]")
    print(f"Music recommendation: [yellow]{', '.join(mood_music[week_mood])}[/yellow]")

    if bool(config.get("Drinks", "enabled")):
        drink = recommend_drink(config, week_mood)
        print(f"Recommended drink for the mood: [yellow]{drink.name}[/yellow]")
        print(f"Ingredients: [yellow]{', '.join(drink.ingredients)}[/yellow]")
        print(f"Garnish: [yellow]{drink.garnish}[/yellow]")
        print(f"Glass: [yellow]{drink.glass}[/yellow]")
        print(f"Instructions: [yellow]{drink.instructions}[/yellow]")

    if bool(config.get("Roon", "enabled")):
        print("[green]Starting playback[/green]")
        if not play_music(config, mood_music[week_mood]):
            print("[red]Sorry, something failed with the playback[/red]")