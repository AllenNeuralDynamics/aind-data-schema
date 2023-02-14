import datetime
from aind_data_schema.imaging import acquisition, tile
from pathlib import Path

def digest_asi_line(line):
    if b'2/' not in line:
        return None
    else:
        mdy, hms, ampm = line.split()[0:3]
        
    mdy = [int(i) for i in mdy.split(b'/')]
    ymd = [mdy[i] for i in [2,0,1]]
    
    
    hms = [int(i) for i in hms.split(b':')]
    if ampm == b'PM':
        hms[0] += 12
    ymdhms = ymd+hms
    dtime = datetime.datetime(*ymdhms)
    ymd = datetime.date(*ymd)
    hms = datetime.time(*hms)
    return dtime

def get_session_end(asi_mdata):
    '''Work backward from the last line until there is a timestamp'''
    idx=-1
    result = None
    while result is None:
        result = digest_asi_line(asi_mdata[idx])
        idx -= 1
    return result

def digest_lc_pos_line(line):
    try:
        result = [int(i) for i in line.split()]
    except:
        return None
    return result

def get_tform(line):
    #x, y, z = line.split()[0:3]
    tform = tile.Translation3dTransform(
        translation=[int(i)/10 for i in line.split()[0:3]]
    )
    return tform

def get_scale(lc_mdata):
    line = lc_mdata[1]
    xy, z = line.split()[3:5]
    scale = tile.Scale3dTransform(
        scale=[xy,xy,z]
    )
    return scale

filter_mapping = {
    488:525,
    561:600,
    647:690
}
def make_acq_tiles(lc_mdata, ):
    channels = {}
    for idx, l in enumerate(lc_mdata[3:6]):
        wavelength, powerl, powerr = [float(j) for j in l.split()]

        channel = tile.Channel(
                channel_name=wavelength,
                laser_wavelength=wavelength,
                laser_power=powerl,
                filter_wheel_index=idx
            )

        channels[wavelength] = channel
        
    scale = get_scale(lc_mdata)
    
    tiles = []
    for line in lc_mdata[8:]:
        X,Y,Z,W,S,E,Sk = [int(i) for i in line.split()]
        tform = get_tform(line)
        channel = channels[float(W)]
        t = tile.AcquisitionTile(
            channel=channel,
            notes='Example generation only -- accuracy not guaranteed.\nLaser power is in percentage of total -- needs calibration',
            coordinate_transformations=[
                tform,
                scale
            ],
            file_name = f'Ex_{W}_Em_{filter_mapping[W]}/{X}/{X}_{Y}/'
        )
        tiles.append(t)
    return tiles


dataset = Path('/Volumes/aind/SmartSPIM_Data/SmartSPIM_651286_2023-02-09_18-44-28/')
raw_data_dir = dataset.joinpath('SmartSPIM')

experimenter = 'Erica Peterson'
subject_id = '651286'

ymd, hms = dataset.name.split('_')[-2:]
ymd = [int(i) for i in ymd.split('-')]
hms = [int(i) for i in hms.split('-')]
session_start_time = ymd+hms
session_start_time = datetime.datetime(*session_start_time)

asi_file = dataset.joinpath('derivatives','ASI_logging.txt')
mdata_file = dataset.joinpath('derivatives','metadata.txt')
with open(asi_file, 'rb') as file:
    asi_mdata = file.readlines()
with open(mdata_file, 'rb') as file:
    lc_mdata = file.readlines()

session_end_time = get_session_end(asi_mdata)

channels = {}
for idx, l in enumerate(lc_mdata[3:6]):
    wavelength, powerl, powerr = [float(j) for j in l.split()]
    
    channel = tile.Channel(
            channel_name=wavelength,
            laser_wavelength=wavelength,
            laser_power=powerl,
            filter_wheel_index=idx
        )
        
    channels[wavelength] = channel

acq = acquisition.Acquisition(
    instrument_id='SmartSPIM01',
    experimenter_full_name=experimenter,
    subject_id=subject_id,
    session_start_time=session_start_time,
    session_end_time=session_end_time,
    local_storage_directory='D:',
    external_storage_directory='',
    chamber_immersion=acquisition.Immersion(
        medium='Cargille',
        refractive_index=1.522,
    ),
    axes=[
        acquisition.Axis(
            name="X",
            dimension=2,
            direction="Left_to_right",
        ),
        acquisition.Axis(
            name="Y",
            dimension=1,
            direction="Posterior_to_anterior"
        ),
        acquisition.Axis(
            name="Z",
            dimension=0,
            direction="Superior_to_inferior"
        ),
    ],
    tiles = make_acq_tiles(lc_mdata)
)

acq.write_standard_file(prefix="smartspim")