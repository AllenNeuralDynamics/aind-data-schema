import os
from typing import Dict, Literal, Union, List

import aind_data_schema.models.devices as d
from pydantic import Field
from aind_data_schema.models.manufacturers import Manufacturer
from aind_data_schema.models.units import SizeUnit


class NewHarpDevice(d.HarpDevice):
    channels: Dict[str, d.DAQChannel] = Field(default_factory=dict)

    def add_channel(self, channel: Union[d.DAQChannel, List[d.DAQChannel]]):
        if isinstance(channel, list):
            for c in channel:
                self.add_channel(c)
        else:
            channel = self._validate_daq_channel(channel)
            self.channels[channel.channel_name] = channel

    def remove_channel(self, channel_name: str):
        if channel_name in self.channels:
            del self.channels[channel_name]
        else:
            raise ValueError(f"Channel {channel_name} does not exist")

    def _validate_daq_channel(self, channel: d.DAQChannel) -> d.DAQChannel:
        if not channel.device_name:
            channel.device_name = self.name
        if channel.device_name != self.name:
            raise ValueError(f"Device name {channel.device_name} does not match {self.name}")
        if channel.channel_name in self.channels:
            raise ValueError(f"Channel {channel.channel_name} already exists")
        return channel


class NewWheel(d.MousePlatform):
    device_type: Literal["Wheel"] = "Wheel"
    radius: float = Field(..., title="Radius (mm)")
    width: float = Field(..., title="Width (mm)")
    size_unit: SizeUnit = Field(SizeUnit.MM, title="Size unit")
    encoder_output: d.DAQChannel = Field(None, title="Encoder DAQ channel")
    pulse_per_revolution: int = Field(..., title="Pulse per revolution")
    brake_output: d.DAQChannel = Field(None, title="Brake DAQ channel")
    torque_output: d.DAQChannel = Field(None, title="Torque DAQ channel")


wheel_encoder_channel = d.DAQChannel(
    device_name='',
    channel_name='DI0', #This should be an array
    channel_type=d.DaqChannelType.DI,
    event_based_sampling=True,
)

wheel_break_channel = d.DAQChannel(
    device_name='',
    channel_name='DO0',
    channel_type=d.DaqChannelType.DO,
    event_based_sampling=True,
)

wheel_torque_channel = d.DAQChannel(
    device_name='',
    channel_name='AI0',
    channel_type=d.DaqChannelType.AI,
    event_based_sampling=True,
)


harp_board = NewHarpDevice(
    name='BehaviorBoard',
    serial_number=None,
    # manufacturer=Manufacturer.CHAMPALIMAUD, # this crashes
    data_interface=d.DataInterface.USB,
    computer_name=os.getenv('COMPUTERNAME'),
    harp_device_type=d.HarpDeviceType.BEHAVIOR,
    is_clock_generator=False,
    port_index='COM3')

harp_board.add_channel(wheel_encoder_channel) # Notice that once this method runs, it modifies the original object with the name of the DaqDevice.
harp_board.add_channel(wheel_break_channel)
harp_board.add_channel(wheel_torque_channel)


new_wheel = NewWheel(
    name='ThisWheel',
    radius=0,
    width=0,
    pulse_per_revolution=0,
    encoder_output=wheel_encoder_channel, # just to show that the object is modified and can be used as a reference
    brake_output=harp_board.channels['DO0'],
    torque_output=harp_board.channels['AI0'],
)
