"""
What it is:
Python code for turning a Matter lightbulb on at 8pm daily, with a random colour.

How to use:
Run the code and wait for 8pm.

Documentation:
https://project-chip.github.io/connectedhomeip-doc/index.html
https://docs.python.org/3/library/subprocess.html
https://schedule.readthedocs.io/en/stable/index.html

Made by:
Jacob Fairhurst
"""

#Imports
import subprocess
import schedule
import time
import random
from datetime import datetime
from typing import Tuple

#Lightbulb constants
NODE_ID = "5467"
ENDPOINT_ID = "1"


def get_random_colour_hue_sat() -> Tuple[int, int]:
    """
    Generate a random hue and saturation value within Matter-compatible ranges.

    Returns:
        Tuple[int, int]: Random hue and saturation values (0–254).
    """
    hue = random.randint(0, 254)
    saturation = random.randint(0, 254)
    return hue, saturation


def turn_on_light_random() -> None:
    """
    Turns on a Matter-compatible smart bulb and sets a random color using
    `chip-tool` command-line calls.

    Assumes:
        - The bulb has already been commissioned and is addressable via chip-tool.
        - The device supports the On/Off and ColorControl clusters.
    """
    hue, saturation = get_random_colour_hue_sat()

    print(f"[{datetime.now()}] Setting hue: {hue}, saturation: {saturation}")

    subprocess.run([
        "chip-tool", "onoff", "on", NODE_ID, ENDPOINT_ID
    ], check=True)

    subprocess.run([
        "chip-tool", "colorcontrol", "move-to-hue", str(hue), "0", "0", "0", NODE_ID, ENDPOINT_ID
    ], check=True)

    subprocess.run([
        "chip-tool", "colorcontrol", "move-to-saturation", str(saturation), "0", "0", "0", NODE_ID, ENDPOINT_ID
    ], check=True)


def main() -> None:
    """
    Schedules the smart light to turn on daily at 8 PM with a random color.
    Keeps the script running to listen for the scheduled time.
    """
    schedule.every().day.at("20:00").do(turn_on_light_random)
    print(f"{datetime.now()}: Scheduler is running. Waiting for 8 PM...")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print(f"\n{datetime.now()}: Scheduler stopped by user.")


if __name__ == "__main__":
    main()