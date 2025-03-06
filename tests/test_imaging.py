""" test Imaging """

import re
import unittest
from datetime import datetime, timezone

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.units import PowerUnit
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components import tile
from aind_data_schema.components.coordinates import (
    Affine3dTransform,
    Rotation,
    Scale,
    Position,
)
from aind_data_schema.components.devices import Calibration, Objective, Laser, ScanningStage
from aind_data_schema.core.acquisition import Acquisition, DataStream
from aind_data_schema.components.configs import Immersion, InVitroImagingConfig
from aind_data_schema.core.processing import DataProcess, ProcessStage, ProcessName
from aind_data_schema.core.instrument import Instrument
from aind_data_schema_models.modalities import Modality
from aind_data_schema.components.identifiers import Person, Code

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class ImagingTests(unittest.TestCase):
    """test imaging schemas"""

    def test_acquisition_constructor(self):
        """testing Acquisition constructor"""
        with self.assertRaises(ValidationError):
            Acquisition()

        a = Acquisition(
            experimenters=[Person(name="alice bob")],
            acquisition_start_time=datetime.now(tz=timezone.utc),
            specimen_id="123456-brain",
            subject_id="123456",
            instrument_id="1234",
            calibrations=[
                Calibration(
                    calibration_date=datetime.now(tz=timezone.utc),
                    description="Laser power calibration",
                    device_name="Laser 1",
                    input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
                    output={
                        "power_measurement": 50.0,
                        "power_unit": PowerUnit.MW,
                    },
                ),
            ],
            acquisition_end_time=datetime.now(tz=timezone.utc),
            data_streams=[
                DataStream(
                    stream_start_time=datetime.now(tz=timezone.utc),
                    stream_end_time=datetime.now(tz=timezone.utc),
                    modalities=[Modality.SPIM],
                    active_devices=[],
                    configurations=[
                        InVitroImagingConfig(
                            chamber_immersion=Immersion(medium="PBS", refractive_index=1),
                            tiles=[
                                tile.AcquisitionTile(
                                    coordinate_transformations=[
                                        Scale(scale=[1, 1, 1]),
                                        Position(translation=[1, 1, 1]),
                                    ],
                                    channel=tile.Channel(
                                        channel_name="488",
                                        light_source_name="Ex_488",
                                        filter_names=["Em_600"],
                                        detector_name="PMT_1",
                                        excitation_wavelength=488,
                                        excitation_power=0.1,
                                        filter_wheel_index=0,
                                    ),
                                )
                            ],
                            axes=[],
                        ),
                    ],
                )
            ],
        )

        self.assertIsNotNone(a)

    def test_instrument_constructor(self):
        """testing Instrument constructor"""
        with self.assertRaises(ValidationError):
            Instrument()

        laser = Laser(
            manufacturer=Organization.HAMAMATSU,
            serial_number="1234",
            name="Laser A",
            wavelength=488,
        )

        objective = Objective(
            name="TLX Objective",
            numerical_aperture=0.2,
            magnification=3.6,
            immersion="multi",
            manufacturer=Organization.THORLABS,
            model="TL4X-SAP",
            notes="Thorlabs TL4X-SAP with LifeCanvas dipping cap and correction optics.",
        )

        scan_stage = ScanningStage(
            name="Sample stage Z",
            model="LS-50",
            manufacturer=Organization.ASI,
            stage_axis_direction="Detection axis",
            stage_axis_name="Z",
            travel=50,
        )

        i = Instrument(
            instrument_id="room_exaSPIM1-1_20231004",
            modalities=[Modality.SPIM],
            instrument_type="diSPIM",
            modification_date=datetime.now().date(),
            manufacturer=Organization.LIFECANVAS,
            components=[objective, laser, scan_stage],
        )

        self.assertIsNotNone(i)

    def test_instrument_type_other_requires_notes(self):
        """testing Instrument type Other requires notes"""
        with self.assertRaises(ValidationError) as e1:
            Instrument(
                instrument_id="room_exaSPIM1-1_20231004",
                modalities=[Modality.SPIM],
                instrument_type="Other",
                modification_date=datetime(2020, 10, 10, 0, 0, 0).date(),
                manufacturer=Organization.OTHER,
                components=[],
            )

        self.assertIn("instrument_id", repr(e1.exception))

    def test_modality_spim_requires_components(self):
        """testing Modality SPIM requires components"""
        with self.assertRaises(ValidationError) as e2:
            Instrument(
                instrument_id="room_exaSPIM1-1_20231004",
                modalities=[Modality.SPIM],
                modification_date=datetime(2020, 10, 10, 0, 0, 0).date(),
                instrument_type="diSPIM",
                manufacturer=Organization.OTHER,
                components=[],
            )

        self.assertIn("modality 'SPIM' requires at least one device", repr(e2.exception))

    def test_axis(self):
        """test the axis class"""
        # test that a few work
        test_codes = ["RAS", "LSP", "RAI", "PAR"]
        for test_code in test_codes:
            a = Acquisition(
                experimenters=[Person(name="alice bob")],
                acquisition_start_time=datetime.now(tz=timezone.utc),
                specimen_id="123456-brain",
                subject_id="123456",
                instrument_id="1234",
                calibrations=[
                    Calibration(
                        calibration_date=datetime.now(tz=timezone.utc),
                        description="Laser power calibration",
                        device_name="Laser 1",
                        input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
                        output={
                            "power_measurement": 50.0,
                            "power_unit": PowerUnit.MW,
                        },
                    ),
                ],
                acquisition_end_time=datetime.now(tz=timezone.utc),
                data_streams=[
                    DataStream(
                        stream_start_time=datetime.now(tz=timezone.utc),
                        stream_end_time=datetime.now(tz=timezone.utc),
                        modalities=[Modality.SPIM],
                        active_devices=[],
                        configurations=[
                            InVitroImagingConfig(
                                chamber_immersion=Immersion(medium="PBS", refractive_index=1),
                                tiles=[
                                    tile.AcquisitionTile(
                                        coordinate_transformations=[
                                            Scale(scale=[1, 1, 1]),
                                            Position(translation=[1, 1, 1]),
                                        ],
                                        channel=tile.Channel(
                                            channel_name="488",
                                            light_source_name="Ex_488",
                                            filter_names=["Em_600"],
                                            detector_name="PMT_1",
                                            excitation_wavelength=488,
                                            excitation_power=0.1,
                                            filter_wheel_index=0,
                                        ),
                                    )
                                ],
                                axes=test_code,
                            ),
                        ],
                    )
                ],
            )
            self.assertEqual(3, len(a.data_streams[0].configurations[0].axes))

    def test_registration(self):
        """test the tile models"""

        t = DataProcess(
            name=ProcessName.IMAGE_TILE_ALIGNMENT,
            stage=ProcessStage.PROCESSING,
            experimenters=[Person(name="Dr. Dan")],
            start_date_time=datetime.now(tz=timezone.utc),
            end_date_time=datetime.now(tz=timezone.utc),
            input_location="/some/path",
            output_location="/some/path",
            code=Code(url="https://github.com/abcd"),
            parameters={
                "tiles": [
                    tile.Tile(
                        coordinate_transformations=[
                            Affine3dTransform(affine_transform=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
                        ]
                    ),
                    tile.Tile(
                        coordinate_transformations=[
                            Position(translation=[0, 1, 2]),
                            Rotation(rotation=[1, 2, 3, 4, 5, 6, 7, 8, 9]),
                            Scale(scale=[1, 2, 3]),
                        ]
                    ),
                ],
            },
            notes="Intra-channel",
        )

        self.assertIsNotNone(t)


if __name__ == "__main__":
    unittest.main()
