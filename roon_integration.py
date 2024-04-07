from roonapi import RoonApi, RoonDiscovery
from pydantic import StrictBool, StrictStr
from typing import List
from configparser import ConfigParser
from time import time, sleep

def play_music(config: ConfigParser, bands: List[StrictStr]) -> StrictBool:
    """Plays a random selection of the bands in the list for a predefined amount of time"""
    if not bool(config.get("Roon", "enabled")):
            return False
    
    appinfo = {
        "extension_id": "FridayMusic",
        "display_name": "Music Recommendation System",
        "display_version": "1.0.0",
        "publisher": config.get("Roon", "publisher"),
        "email": config.get("Roon", "email")
    }
    play_duration = int(config.get("Roon", "play_time_minutes")) * 60
    target_zone = config.get("Roon", "target_zone")

    try:
        core_id = open(config.get("Roon", "id_file")).read()
        token = open(config.get("Roon", "token_file")).read()
    except OSError:
        print("Please authorize first using discovery.py in the examples directory of the https://github.com/pavoni/pyroon repo.")
        exit()

    discover = RoonDiscovery(core_id)
    server = discover.first()
    discover.stop()

    roonapi = RoonApi(appinfo, token, server[0], server[1], True)

    zones = roonapi.zones
    output_id = [output["zone_id"] for output in zones.values() if output["display_name"] == target_zone][0]

    start_time = time()
    try:
        for band in bands:
            items = roonapi.play_media(
                output_id, ["Library", "Artists", band], "Queue"
            )
        
        while time() - start_time < play_duration:
            sleep(1)
        roonapi.playback_control("pause")
        print(f"Playback stopped after {play_duration} seconds.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return True