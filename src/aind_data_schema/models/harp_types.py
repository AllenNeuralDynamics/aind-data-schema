"""Module for Harp Device Types"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated

class _HarpDeviceType(PIDName):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class Behavior(_HarpDeviceType):
    """Behavior"""

    name = "Behavior"
    whoami = 1216


class CameraController(_HarpDeviceType):
    """Camera Controller"""

    name = "Camera Controller"
    whoami = 1168


class ClockSynchronizer(_HarpDeviceType):
    """Clock Synchronizer"""

    name = "Clock Synchronizer"
    whoami = 1152


class InputExpander(_HarpDeviceType):
    """Input Expander"""

    name = "Input Expander"
    whoami = 1106


class LoadCells(_HarpDeviceType):
    """Load Cells"""

    name = "Load Cells"
    whoami = 1232


class Olfactometer(_HarpDeviceType):
    """Olfactometer"""

    name = "Olfactometer"
    whoami = 1140


class SoundCard(_HarpDeviceType):
    """Sound Card"""

    name = "Sound Card"
    whoami = 1280


class Synchronizer(_HarpDeviceType):
    """Synchronizer"""

    name = "Synchronizer"
    whoami = 1104


class TimestampGeneratorGen1(_HarpDeviceType):
    """Timestamp Generator Gen 1"""

    name = "Timestamp Generator Gen 1"
    whoami = 1154


class TimestampGeneratorGen3(_HarpDeviceType):
    """Timestamp Generator Gen 3"""

    name = "Timestamp Generator Gen 3"
    whoami = 1158


class HarpDeviceType:
    """Harp device type definitions"""

    BEHAVIOR = Behavior()
    CAMERA_CONTROLLER = CameraController()
    CLOCK_SYNCHRONIZER = ClockSynchronizer()
    INPUT_EXPANDER = InputExpander()
    LOAD_CELLS = LoadCells()
    OLFACTOMETER = Olfactometer()
    SOUND_CARD = SoundCard()
    SYNCHRONIZER = Synchronizer()
    TIMESTAMP_GENERATOR_1 = TimestampGeneratorGen1()
    TIMESTAMP_GENERATOR_3 = TimestampGeneratorGen3()

    _ALL = tuple(_HarpDeviceType.__subclasses__())
    ONE_OF = Annotated[Union[_ALL], Field(discriminator="name")]
    
