"""Module for Harp Device Types"""

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class _HarpDeviceType(BaseModel):
    """Base model config"""

    model_config = ConfigDict(frozen=True)
    name: str
    whoami: int


class Behavior(_HarpDeviceType):
    """Behavior"""

    name: Literal["Behavior"] = "Behavior"
    whoami: Literal[1216] = 1216


class CameraController(_HarpDeviceType):
    """Camera Controller"""

    name: Literal["Camera Controller"] = "Camera Controller"
    whoami: Literal[1168] = 1168


class ClockSynchronizer(_HarpDeviceType):
    """Clock Synchronizer"""

    name: Literal["Clock Synchronizer"] = "Clock Synchronizer"
    whoami: Literal[1152] = 1152


class GenericHarpDevice(_HarpDeviceType):
    """Generic Harp Device"""

    name: Literal["Generic Harp Device"] = "Generic Harp Device"
    whoami: int = Field(default=0, ge=0, le=9999, title="WhoAmI")


class InputExpander(_HarpDeviceType):
    """Input Expander"""

    name: Literal["Input Expander"] = "Input Expander"
    whoami: Literal[1106] = 1106


class LoadCells(_HarpDeviceType):
    """Load Cells"""

    name: Literal["Load Cells"] = "Load Cells"
    whoami: Literal[1232] = 1232


class Olfactometer(_HarpDeviceType):
    """Olfactometer"""

    name: Literal["Olfactometer"] = "Olfactometer"
    whoami: Literal[1140] = 1140


class SoundCard(_HarpDeviceType):
    """Sound Card"""

    name: Literal["Sound Card"] = "Sound Card"
    whoami: Literal[1280] = 1280


class Synchronizer(_HarpDeviceType):
    """Synchronizer"""

    name: Literal["Synchronizer"] = "Synchronizer"
    whoami: Literal[1104] = 1104


class TimestampGeneratorGen1(_HarpDeviceType):
    """Timestamp Generator Gen 1"""

    name: Literal["Timestamp Generator Gen 1"] = "Timestamp Generator Gen 1"
    whoami: Literal[1154] = 1154


class TimestampGeneratorGen3(_HarpDeviceType):
    """Timestamp Generator Gen 3"""

    name: Literal["Timestamp Generator Gen 3"] = "Timestamp Generator Gen 3"
    whoami: Literal[1158] = 1158


class LicketySplit(_HarpDeviceType):
    """Lickety Split"""

    name: Literal["Lickety Split"] = "Lickety Split"
    whoami: Literal[1400] = 1400


class SniffDetector(_HarpDeviceType):
    """Sniff Detector"""

    name: Literal["Sniff Detector"] = "Sniff Detector"
    whoami: Literal[1401] = 1401


class Treadmill(_HarpDeviceType):
    """Treadmill"""

    name: Literal["Treadmill"] = "Treadmill"
    whoami: Literal[1402] = 1402


class Cuttlefish(_HarpDeviceType):
    """Cuttlefish"""

    name: Literal["Cuttlefish"] = "Cuttlefish"
    whoami: Literal[1403] = 1403


class StepperDriver(_HarpDeviceType):
    """Stepper Driver"""

    name: Literal["Stepper Driver"] = "Stepper Driver"
    whoami: Literal[1130] = 1130


class HarpDeviceType:
    """Harp device type definitions"""

    BEHAVIOR = Behavior()
    GENERIC_HARP_DEVICE = GenericHarpDevice()
    CAMERA_CONTROLLER = CameraController()
    CLOCK_SYNCHRONIZER = ClockSynchronizer()
    INPUT_EXPANDER = InputExpander()
    LOAD_CELLS = LoadCells()
    OLFACTOMETER = Olfactometer()
    SOUND_CARD = SoundCard()
    SYNCHRONIZER = Synchronizer()
    TIMESTAMP_GENERATOR_1 = TimestampGeneratorGen1()
    TIMESTAMP_GENERATOR_3 = TimestampGeneratorGen3()
    LICKETY_SPLIT = LicketySplit()
    SNIFF_DETECTOR = SniffDetector()
    TREADMILL = Treadmill()
    CUTTLEFISH = Cuttlefish()
    STEPPER_DRIVER = StepperDriver()

    _ALL = tuple(_HarpDeviceType.__subclasses__())
    ONE_OF = Annotated[Union[_ALL], Field(discriminator="name")]
