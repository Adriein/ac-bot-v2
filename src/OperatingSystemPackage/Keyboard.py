from typing import Iterable

from Xlib import X, display, XK
from Xlib.protocol import event
import pyautogui

from src.OperatingSystemPackage import Kernel


class Keyboard:
    def __init__(self, kernel: Kernel):
        self.__kernel = kernel

    def press(self, key: str | Iterable[str]):
        """
        tibia_window_id = self.__kernel.tibia_window_id()

        # Create a connection to the X server
        d = display.Display()

        # Get the target window using its ID
        window = d.create_resource_object('window', tibia_window_id)

        keycode = d.keysym_to_keycode(XK.string_to_keysym(key))
        time = X.CurrentTime
        key_press_event = event.KeyPress(
            time=time,
            root=d.screen().root.id,
            window=tibia_window_id,
            same_screen=0,
            child=X.PointerRoot,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=0,
            detail=keycode
        )
        window.send_event(key_press_event, propagate=True)

        key_release_event = event.KeyRelease(
            time=time,
            root=d.screen().root.id,
            window=tibia_window_id,
            same_screen=0,
            child=X.PointerRoot,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=0,
            detail=keycode
        )
        d.send_event(tibia_window_id, key_release_event, propagate=False)

        # Sync to make sure the event is processed
        d.flush()
        """
        pyautogui.press(keys=key, interval=0.0, _pause=False)

    def key_down(self, key: str) -> None:
        pyautogui.keyDown(key)

    def key_up(self, key: str) -> None:
        pyautogui.keyUp(key)
