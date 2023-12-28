""" This module contains functions related to screenshots of the DS screens. """
import pyautogui
import numpy as np
from PIL import Image

from settings import settings as s

def get_ds_game_screen(screenshot: Image) -> Image:
    """Get the DS game screen from a screenshot.

    Args:
        screenshot (Image): screenshot of the screen where DeSmuME is running.

    Returns:
        Image: _description_
    """
    w_screen, h_screen = screenshot.size

    # define the area of the DS game screen
    y = h = h_screen // 2
    x = w = w_screen // 3
    area = (x, y, x + w, y + h)

    # Crop the screenshot to only show the DS game screen.
    ds_game_screen = screenshot.crop(area)
    return ds_game_screen

def take_screenshot(main_screen: bool =True) -> Image:
    """Take a screenshot of the game screens based on which screen they are on.

    Args:
        main_screen (bool, optional): whether DeSmuME is running on the main \
            screen (principal display) or not. Defaults to True.

    Returns:
        ds_game_screen(Image): screenshot of the DS game screens.
    """
    region = s.MAIN_SCREEN if main_screen else s.SUB_SCREEN
    screenshot = pyautogui.screenshot(region=region)
    size = screenshot.size
    scale = s.MAIN_SCREEN_SCALE if main_screen else\
        s.SUB_SCREEN_SCALE
    # Scales image to match original DS screen size.
    screenshot = screenshot.resize( ( int(size[0] / scale),
        int(size[1] / scale) ))
    print(f"Screenshot taken from {region} with size {screenshot.size}")
    ds_game_screen = get_ds_game_screen(screenshot)
    return ds_game_screen

def local_2_global_position(bbox: np.ndarray, main_screen: bool = True) -> tuple:
    """Convert a position on the subscreen to a position on the total screen.

    Args:
        bbox (np.ndarray): bounding box of the detection coordinates in xywh \
            format. These coordinates are relative to the screen showing \
            DeSmuME. Must be in ccwh format. Shape: (4,).
        main_screen (bool, optional): whether DeSmuME is running on the main \
            screen or not. Defaults to True.

    Returns:
        global_bbox(np.ndarray): position of the bounding box on the total screen, \
            which is composed of the main and sub screens. The bounding box \
            is in ccwh format. Shape: (4,).
    """
    scale = s.MAIN_SCREEN_SCALE if main_screen else s.SUB_SCREEN_SCALE

    # local 2 screen coordinates system:
    x, y, w, h = bbox
    offset_1 = s.MAIN_SCREEN if main_screen else s.SUB_SCREEN
    off_1_x, off_1_y = offset_1[2]//3, offset_1[3]//2
    x_screen, y_screen = x + off_1_x, y + off_1_y

    # screen 2 global screen coordinates system:
    offset_2 = s.MAIN_SCREEN if main_screen else s.SUB_SCREEN
    global_bbox = np.array([x_screen, y_screen, w, h]) * scale + np.array([offset_2[0], offset_2[1], 0, 0])

    return global_bbox
