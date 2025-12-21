from .command_elements_liha import *
from .command_elements_mca import *

class TecanCommand():
    def __init__(self):
        self._api_channel = None
        pass

    def set_api_channel(api_channel):
        self._api_channel = api_channel
    
    def run(self):
        if api_channel is None:
            raise RuntimeError("API channel is not provided")
        self._api_channel.ExecuteCommand(self.cmd())

class AddLabware(TecanCommand):
    def __init__(self, label: str, type: str,
                    location: str, position: int,
                    rotation: int = 0):
        super().__init__()

    def __str__(self):
        pass

    def cmd(self):

