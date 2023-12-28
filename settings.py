" Settings for the AI-Mario-Party project."
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Base Settings for configuring the AI-Mario-Party project.
    
    To configure the settings in this project the [BaseSettings class from
    pydantic is used](https://docs.pydantic.dev/usage/settings/).
    This class will read the environment variables and will validate them.

    !!! Abstract "Environment Variables to configure the project."
        The following table shows the environment variables that
            can be used to configure the project:

        | Environment Variable | Description | Default |
        |----------------------|-------------| ------- |
        | SECONDARY_DISPLAY| If there are two screens, this variable must \
            be set to True. | False |
        | MAIN_SCREEN | Main screen location on the total screen. [TL_x, TL_y, w, h] \
            | [ 0, 0, 1920, 1080 ] |
        | MAIN_SCREEN_SCALE | Scale of the main screen. | 1.0 |
        | SUB_SCREEN | Secondary screen location on the total screen. \
            [TL_x, TL_y, w, h]. If there is no second screen, leave its \
            default value. | [ 1920, 1080, 1920, 1080 ] |
        | SUB_SCREEN_SCALE | Scale of the second screen. If there is no second \
            screen, leave its default value. | 1.0 |
        | DS_WIDTH | Width of the standard DS screen. | 256 |
        | DS_HEIGHT | Height of the standard DS screen. | 192 |
    """
    SECONDARY_DISPLAY: bool = False

    MAIN_SCREEN: List = [0, 0, 1920, 1080]
    MAIN_SCREEN_SCALE: float = 1.0

    SUB_SCREEN: List = [1920, 0, 1920, 1080]
    SUB_SCREEN_SCALE: int = 1.0

    DS_WIDTH: int = 256
    DS_HEIGHT: int = 192

settings = Settings()
