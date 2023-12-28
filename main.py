"""The main file for the AI-Mario-Party program."""
import time
import sys

import pyautogui

from src import *

game_names = ["Goomba wrangler"]
game_scripts = [name.replace(" ", "_").title() for name in game_names]
game_script_index = 1


if __name__ == "__main__":
    # Confirmation box to start the program.
    selected_button = pyautogui.confirm(
        "Select a minigame to have the AI play.",
        title="AI Mario Party",
        buttons=game_names + ["Cancel"]
    )

    if selected_button == "Cancel" or selected_button is None:
        sys.exit()
    elif selected_button == "Goomba wrangler":
        from src.goomba_wrangler import invoke_ai

    timeout = time.time() + 30   # 30 seconds from now
    i = 0
    while True:
        invoke_ai(main_screen=False)
        if time.time() > timeout:
            break
        i += 1
