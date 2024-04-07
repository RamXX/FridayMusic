from enum import Enum

class Mood(Enum):
    HAPPY = 1
    EXCITED = 2
    CONTENT = 3
    RELAXED = 4
    BORED = 5
    TIRED = 6
    STRESSED = 7
    ANXIOUS = 8
    FRUSTRATED = 9
    ANGRY = 10
    SAD = 11
    DEPRESSED = 12
    HOPEFUL = 13
    MOTIVATED = 14
    INSPIRED = 15
    CONFUSED = 16
    SURPRISED = 17
    NOSTALGIC = 18
    GUILTY = 19
    EMBARRASSED = 20
    NEUTRAL = 21

# Change to fit your taste.
# This is a proud GenXer's list 💪
mood_music = {
    Mood.HAPPY: ["The Beach Boys", "The Beatles", "Katrina and The Waves", "Bobby McFerrin"],
    Mood.EXCITED: ["AC/DC", "Van Halen", "Guns N' Roses", "Twisted Sister", "ZZ Top", "Slash"],
    Mood.CONTENT: ["Dire Straits", "Bob Marley", "The Eagles", "Pink Floyd"],
    Mood.RELAXED: ["Bill Evans", "Miles Davis", "John Coltrane", "Frank Sinatra"],
    Mood.BORED: ["The Cure", "Joy Division", "Depeche Mode", "The Smiths"],
    Mood.TIRED: ["Simon & Garfunkel", "Bob Dylan", "Leonard Cohen", "Nick Drake"],
    Mood.STRESSED: ["Metallica", "Megadeth", "Slayer", "Pantera"],
    Mood.ANXIOUS: ["Pink Floyd", "Radiohead", "Nine Inch Nails", "Tool"],
    Mood.FRUSTRATED: ["Rage Against the Machine", "Nirvana", "Pearl Jam", "Alice in Chains"],
    Mood.ANGRY: ["Metallica", "Slipknot", "Pantera", "Sepultura"],
    Mood.SAD: ["Eric Clapton", "B.B. King", "Billie Holiday", "Nina Simone"],
    Mood.DEPRESSED: ["Joy Division", "The Smiths", "Nirvana", "Alice in Chains"],
    Mood.HOPEFUL: ["Journey", "Bon Jovi", "Survivor", "Europe"],
    Mood.MOTIVATED: ["Survivor", "Queen", "Aerosmith", "Twisted Sister"],
    Mood.INSPIRED: ["Pink Floyd", "Led Zeppelin", "The Beatles", "David Bowie"],
    Mood.CONFUSED: ["Pink Floyd", "Yes", "King Crimson", "Rush"],
    Mood.SURPRISED: ["Frank Zappa", "Primus", "Mr. Bungle", "Faith No More"],
    Mood.NOSTALGIC: ["The Beatles", "The Rolling Stones", "The Beach Boys", "Elvis Presley"],
    Mood.GUILTY: ["Johnny Cash", "The Clash", "The Ramones", "Sex Pistols"],
    Mood.EMBARRASSED: ["The Cure", "Morrissey", "The Smiths", "Depeche Mode"],
    Mood.NEUTRAL: ["Pink Floyd"]
}

# Since the goal is to play music on Friday, the closest the day 
# is to Friday, the more weight it has for the mood of the week.
day_weights = {
        0: 0.05,  # Monday
        1: 0.10,  # Tuesday
        2: 0.20,  # Wednesday
        3: 0.25,  # Thursday
        4: 0.40,  # Friday
        5: 0.00,  # Saturday
        6: 0.00   # Sunday
}