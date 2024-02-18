import os
import aind_data_schema.models.devices as d
from aind_data_schema.models.manufacturers import Manufacturer



wheel_encoder_channel = d.DAQChannel(
    device_name='BehaviorBoard',
    channel_name='DI0', #This should be an array
    channel_type=d.DaqChannelType.DI,
    event_based_sampling=True,
)

wheel_break_channel = d.DAQChannel(
    device_name='BehaviorBoard',
    channel_name='DO0',
    channel_type=d.DaqChannelType.DO,
    event_based_sampling=True,
)

wheel_torque_channel = d.DAQChannel(
    device_name='BehaviorBoard',
    channel_name='AI0',
    channel_type=d.DaqChannelType.AI,
    event_based_sampling=True,
)


harp_board = d.HarpDevice(
    name='BehaviorBoard',
    serial_number=None,
    # manufacturer=Manufacturer.CHAMPALIMAUD, # this crashes
    data_interface=d.DataInterface.USB,
    computer_name=os.getenv('COMPUTERNAME'),
    channels=[wheel_encoder_channel, wheel_break_channel, wheel_torque_channel],
    harp_device_type=d.HarpDeviceType.BEHAVIOR,
    is_clock_generator=False,
    port_index='COM3')


wheel = d.Wheel(
    name='ThisWheel',
    encoder=harp_board,
    encoder_output=harp_board.channels[0],
    magnetic_brake=harp_board,
    brake_output=harp_board.channels[1],
    torque_sensor=harp_board,
    torque_output=harp_board.channels[2],
    radius=0,
    width=0,
    pulse_per_revolution=0,
)