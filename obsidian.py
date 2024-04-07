import os
import re
import dspy

from pydantic import BaseModel, StrictStr, StrictInt
from typing import Tuple, List
from collections import defaultdict
from datetime import datetime, timedelta

from config import Mood, day_weights

#
# Pydantic classes first
#
class DailyNote(BaseModel):
    date: StrictStr
    dow: StrictInt # Day of the week, where 0=Monday, 6=Sunday
    content: StrictStr
    mood: Mood
#
# DSPy classes
#
class MoodSignature(dspy.Signature):
    """Assign the most appropriate mood associated with the content"""
    content: StrictStr = dspy.InputField(desc="Text being analyzed")
    mood: Mood = dspy.OutputField(desc="Numeric representation of the mood according to Enum provided. Only output a number, nothing else. If no mood matches perfectly, choose 21 (NEUTRAL)")

def process_obsidian_notes(directory: StrictStr) -> Mood:
    """Reads the daily notes from the last 7 days and assigns a mood to each. Returns the mood for the week"""
    if directory is None:
        raise ValueError("Obsidian Daily Notes directory cannot be empty. Please specify it in your config.ini file.")
    notes = []
    mooder = dspy.TypedChainOfThought(MoodSignature)
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            date_str = filename.split(" ")[0].split(".")[0]  # In Daily Notes, the filename is the date. We assume it's in YYYY-MM-DD format.
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if one_week_ago <= date <= today:
                file_path = os.path.join(directory, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                except FileNotFoundError:
                    print(f"File {file_path} not found. Please check the file path.")
                    continue
                except PermissionError:
                    print(f"Permission denied. You don't have sufficient permissions to access the file {file_path}.")
                    continue
                except OSError as e:
                    print(f"An error occurred while accessing the file: {str(e)}")
                    continue
                except UnicodeDecodeError:
                    print("Error decoding the file. Please check the file encoding.")
                    continue
                content = remove_markdown(content)

                dow = date.weekday()  # Calculate the day of the week (0 = Monday, 6 = Sunday)
                mood_prediction = mooder(content=content)
                note = DailyNote(date=date_str, dow=dow, content=content, mood=mood_prediction.mood)
                notes.append(note)
    week_mood = calculate_week_mood(notes)
    return week_mood

def remove_markdown(content: StrictStr) -> StrictStr:
    """Remove Markdown links, keeping only the description"""
    content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
    content = re.sub(r"#+ ", "", content)
    content = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", content)

    return content.strip()

def calculate_week_mood(daily_notes: List[DailyNote]) -> Mood:
    """Calculate the mood for the week based on pre-defined weights"""
    mood_scores: defaultdict = defaultdict(float)

    for note in daily_notes:
        mood = note.mood
        day_weight = day_weights[note.dow]
        mood_scores[mood] += day_weight

    if mood_scores:
        week_mood = max(mood_scores, key=mood_scores.get)
        return week_mood
    else:
        return Mood(Mood.NEUTRAL)