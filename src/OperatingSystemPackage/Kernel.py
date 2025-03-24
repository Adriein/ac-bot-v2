import os
import signal

from .Console import Console
from .Exception.CommandExecutionException import CommandExecutionException

from src.LoggerPackage import Logger
from src.UtilPackage import Array


class Kernel:
    TIBIA_WINDOW_NAME = "Tibia"
    OBS_TIBIA_PREVIEW_WINDOW_NAME = "Projector"
    TIBIA_PID_BIN_PATH = "gmbh/tibia/packages/tibia/bin"

    def __init__(self):
        self.__tibia_window_id = self.__get_tibia_window_id()
        # self.__obs_tibia_preview_window_id = self.__get_obs_tibia_preview_window_id()

    def tibia_window_id(self) -> int:
        return self.__tibia_window_id

    def obs_tibia_preview_window_id(self) -> int:
        return self.__obs_tibia_preview_window_id

    def force_game_logout(self) -> None:
        os.kill(self.__tibia_bin_pid, signal.SIGTERM)

    def __get_tibia_window_id(self) -> int:
        try:
            window_ids = Console.execute(fr'xdotool search --name "\b"{self.TIBIA_WINDOW_NAME}"\b"')
            window_ids_parsed_result = list(filter(None, window_ids.split('\n')))

            if Array.is_array(window_ids_parsed_result):
                for window_id in window_ids_parsed_result:
                    try:
                        window_pid = Console.execute(f'xdotool getwindowpid {window_id}')

                        pid_info = Console.execute(f'pwdx {window_pid}')

                        self.__tibia_bin_pid = int(pid_info[:pid_info.find(":")])

                        if self.TIBIA_PID_BIN_PATH in pid_info.lower():
                            return int(window_id)

                    except CommandExecutionException:
                        continue

        except CommandExecutionException as exception:
            Logger.error(str(exception), exception)
            raise SystemExit

    def __get_obs_tibia_preview_window_id(self) -> int:
        try:
            window_id = Console.execute(fr'xdotool search --name "\b"{self.OBS_TIBIA_PREVIEW_WINDOW_NAME}"\b"')

            if not window_id:
                raise Exception

            return int(window_id)

        except CommandExecutionException as exception:
            Logger.error(str(exception), exception)
            raise SystemExit
