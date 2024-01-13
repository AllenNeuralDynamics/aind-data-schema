"""Module for Harp Device Types"""

from typing import Literal, Union

from pydantic import ConfigDict, Field
from typing_extensions import Annotated


class _HarpDeviceType(AindModel):
    """Base model config"""

    model_config = ConfigDict(frozen=True)


class Behavior(_HarpDeviceType):
    """Behavior"""

    name = Literal["Behavior"] = "Behavior"
    whoami = 1216


class CameraController(_HarpDeviceType):
    """Camera Controller"""

    name = Literal["Camera Controller"] = "Camera Controller"
    whoami = 1168


class ClockSynchronizer(_HarpDeviceType):
    """Clock Synchronizer"""

    name = Literal["Clock Synchronizer"] = "Clock Synchronizer"
    whoami = 1152


class InputExpander(_HarpDeviceType):
    """Input Expander"""

    name = Literal["Input Expander"] = "Input Expander"
    whoami = 1106


class LoadCells(_HarpDeviceType):
    """Load Cells"""

    name = Literal["Load Cells"] = "Load Cells"
    whoami = 1232


class Olfactometer(_HarpDeviceType):
    """Olfactometer"""

    name = Literal["Olfactometer"] = "Olfactometer"
    whoami = 1140


class SoundCard(_HarpDeviceType):
    """Sound Card"""

    name = Literal["Sound Card"] = "Sound Card"
    whoami = 1280


class Synchronizer(_HarpDeviceType):
    """Synchronizer"""

    name = Literal["Synchronizer"] = "Synchronizer"
    whoami = 1104


class TimestampGeneratorGen1(_HarpDeviceType):
    """Timestamp Generator Gen 1"""

    name = Literal["Timestamp Generator Gen 1"] = "Timestamp Generator Gen 1"
    whoami = 1154


class TimestampGeneratorGen3(_HarpDeviceType):
    """Timestamp Generator Gen 3"""

    name = Literal["Timestamp Generator Gen 3"] = "Timestamp Generator Gen 3"
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
