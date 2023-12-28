import math
from ultralytics import YOLO
from scipy.spatial import distance as dist

from src.screen_utils import *

refresh_rate = 20
model = YOLO('models/train2/weights/best.pt')
pyautogui.MINIMUM_DURATION = 0.02
pyautogui.PAUSE = 0.02

def circle_area(goomba_centre:tuple, radius: float):
    """Draw a circle on the screen around a goomba's bounding box.
    
    We use the library pyautogui to move the mouse on the screen. This library
    can only move the mouse from point A to point B, so we need to find the 
    vertices of a poligon with "a lot" of sides and then connect the dots. The 
    more vertices the poligon has, the more it will look like a circle.

    Args:
        goomba_centre (tuple): centre of the goomba's bounding box.
        radius (float): radius of the circle to be dawn.
    """
    points = 10
    arc_length = 360 // points
    is_first_point_in_circle = True
    for angle in range(0, 365 + arc_length * 2, arc_length):
        radians = angle / (180 / math.pi)
        offset = (radius * math.cos(radians), radius * math.sin(radians))
        position = (goomba_centre[0] + offset[0], goomba_centre[1] + offset[1])
        if is_first_point_in_circle:
            pyautogui.moveTo(position[:2], duration = 0.05, _pause=False)
            pyautogui.mouseDown()
            is_first_point_in_circle = False
        pyautogui.moveTo(position[:2], duration = 0.05, _pause=False)
    pyautogui.mouseUp()

def select_goomba(detections, screen_shape: tuple) -> list:
    """Select the goomba that we want to circle.
    
    Discard goombas in the perifery of the screen and select the goomba that is
    furthest away from any bomb.

    Args:
        detections (np.ndarray): bounding boxes of the goombas and bombs.
        screen_shape (tuple): shape of the screen.

    Returns:
        target_goomba(list): bounding box of the goomba to circle in xywh format.
    """
    goomba_bbox = []
    bomb_bbox = []
    for det in detections:
        x, y, w, h = det.boxes.xywh.numpy().astype(int)[0]
        if det.boxes.cls.numpy() == 1:
            bomb_bbox.append([x, y, w, h])
        else:
            is_in_perifery = (
                (x < 0.3 * screen_shape[0]) or (x > 0.7 * screen_shape[0])
            ) or (
                (y < 0.3 * screen_shape[1]) or (y > 0.7 * screen_shape[1])
            )
            if not is_in_perifery:
                goomba_bbox.append([x, y, w, h])

    # Select the goomba that is furthest away from any bomb
    min_distance_to_bomb = 100
    target_goomba = None
    for goomba in goomba_bbox:
        goomba_center = goomba[:2]
        distances = [dist.euclidean(goomba_center, bomb[:2]) for bomb in bomb_bbox]
        if not any(d < min_distance_to_bomb for d in distances):
            target_goomba = goomba
            break
    return target_goomba

def invoke_ai(main_screen: bool = True):
    """Call the AI to play Goomba wragler. 
    
    A yolov8 model will circle the goomba that is furthest away from any bomb.

    Args:
        main_screen (bool, optional): whether DeSmuME is running on the main \
            screen (principal display) or not. Defaults to True.
    """
    ds_game_screen = take_screenshot(main_screen=main_screen)
    ds_game_screen = np.array(ds_game_screen)
    detections = model([ds_game_screen])[0]
    target_goomba = select_goomba(detections, ds_game_screen.shape)

    if target_goomba is not None:
        goomba_global_bbox = local_2_global_position(target_goomba, main_screen=main_screen)
        goomba_center = goomba_global_bbox[:2]
        radius = int(goomba_global_bbox[2])+20
        circle_area(goomba_center, radius)
        return
