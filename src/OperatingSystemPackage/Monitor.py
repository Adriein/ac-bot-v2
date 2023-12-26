import cv2
import numpy
from PIL import Image
from Xlib import display, X

from .Kernel import Kernel

from src.VendorPackage import PyAutoGui


class Monitor:
    IMAGE_MODE = 'RGB'
    DECODER = 'raw'
    ORDER = 'BGRX'

    def __init__(self, kernel: Kernel, pyautogui: PyAutoGui):
        [width, height] = pyautogui.screen_size()
        self.__width = width
        self.__height = height
        self.__kernel = kernel

    def screenshot(self) -> numpy.ndarray:
        obs_tibia_preview_window_id = self.__kernel.obs_tibia_preview_window_id()

        # Create a connection to the X server
        disp = display.Display()

        # Get the specified window
        window = disp.create_resource_object('window', obs_tibia_preview_window_id)

        # Get the dimensions of the window
        width = window.get_geometry().width
        height = window.get_geometry().height

        # Get the raw image data from the window
        raw = window.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)

        # Convert the raw image data to a PIL Image object
        image = Image.frombytes(
            self.IMAGE_MODE,
            (width, height),
            raw.data,
            self.DECODER,
            self.ORDER
        )

        disp.close()

        return cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)

    def specifications(self) -> tuple[int, int]:
        return self.__width, self.__height
