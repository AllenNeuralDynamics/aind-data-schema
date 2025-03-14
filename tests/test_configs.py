""" Tests for the configs module """

import unittest
from decimal import Decimal
from pydantic import ValidationError
from aind_data_schema.components.configs import MRIScan, Rotation, Translation, Scale, ManipulatorConfig
from aind_data_schema.components.coordinates import FloatAxis, AxisName, Coordinate, SurfaceCoordinate
from aind_data_schema_models.brain_atlas import CCFStructure
from aind_data_schema_models.units import AngleUnit


class TestMRIScan(unittest.TestCase):
    """Tests for the MRIScan class"""

    def test_validate_primary_scan_success(self):
        """Test validate_primary_scan method with valid primary scan data"""
        scan = MRIScan(
            device_name="MRI Scanner",
            scan_index=1,
            scan_type="3D Scan",
            primary_scan=True,
            scan_sequence_type="RARE",
            echo_time=Decimal("10.0"),
            repetition_time=Decimal("2000.0"),
            subject_position="Prone",
            additional_scan_parameters={},
            vc_orientation=Rotation(
                angles=[
                    FloatAxis(value=1.0, axis=AxisName.AP),
                    FloatAxis(value=1.0, axis=AxisName.SI),
                    FloatAxis(value=1.0, axis=AxisName.ML),
                ],
                order=[AxisName.AP, AxisName.SI, AxisName.ML],
            ),
            vc_position=Translation(
                translation=[
                    FloatAxis(value=1.0, axis=AxisName.AP),
                    FloatAxis(value=1.0, axis=AxisName.SI),
                    FloatAxis(value=1.0, axis=AxisName.ML),
                ]
            ),
            voxel_sizes=Scale(
                scale=[
                    FloatAxis(value=0.5, axis=AxisName.AP),
                    FloatAxis(value=0.4375, axis=AxisName.SI),
                    FloatAxis(value=0.52, axis=AxisName.ML),
                ]
            ),
        )
        self.assertIsNotNone(scan)

    def test_validate_primary_scan_failure(self):
        """Test validate_primary_scan method with invalid primary scan data"""
        invalid_data = {
            "device_name": "MRI Scanner",
            "scan_index": 1,
            "scan_type": "3D Scan",
            "primary_scan": True,
            "scan_sequence_type": "RARE",
            "echo_time": Decimal("10.0"),
            "repetition_time": Decimal("2000.0"),
            "subject_position": "Prone",
            "additional_scan_parameters": {},
        }
        with self.assertRaises(ValidationError):
            MRIScan(**invalid_data)


class TestManipulatorConfig(unittest.TestCase):
    """Tests for the ManipulatorConfig class"""

    def test_validate_len_coordinates_success(self):
        """Test validate_len_coordinates method with valid coordinate lengths"""
        coordinate1 = Coordinate(
            system_name="Bregma ARI",
            position=[
                FloatAxis(value=1.0, axis=AxisName.AP),
                FloatAxis(value=2.0, axis=AxisName.ML),
                FloatAxis(value=3.0, axis=AxisName.SI),
            ]
        )
        coordinate2 = Coordinate(
            system_name="Bregma ARI",
            position=[
                FloatAxis(value=4.0, axis=AxisName.X),
                FloatAxis(value=5.0, axis=AxisName.Y),
                FloatAxis(value=6.0, axis=AxisName.Z),
            ]
        )
        coordinate1_surface = SurfaceCoordinate(
            system_name="Bregma ARI",
            position=[
                FloatAxis(value=1.0, axis=AxisName.AP),
                FloatAxis(value=2.0, axis=AxisName.ML),
                FloatAxis(value=3.0, axis=AxisName.SI),
            ],
            depth=1,
        )
        coordinate2_surface = SurfaceCoordinate(
            system_name="Bregma ARI",
            position=[
                FloatAxis(value=4.0, axis=AxisName.X),
                FloatAxis(value=5.0, axis=AxisName.Y),
                FloatAxis(value=6.0, axis=AxisName.Z),
            ],
            depth=2,
        )
        config = ManipulatorConfig(
            device_name="Manipulator",
            arc_angle=Decimal("45.0"),
            module_angle=Decimal("30.0"),
            angle_unit=AngleUnit.DEG,
            primary_targeted_structure=CCFStructure.HPF,
            atlas_coordinates=[coordinate1, coordinate2],
            manipulator_coordinates=[coordinate1_surface, coordinate2_surface],
            manipulator_axis_positions=[coordinate1, coordinate2],
        )
        self.assertIsInstance(config, ManipulatorConfig)

    def test_validate_len_coordinates_failure(self):
        """Test validate_len_coordinates method with invalid coordinate lengths"""

        with self.assertRaises(ValueError) as context:
            ManipulatorConfig(
                device_name="Manipulator",
                arc_angle=Decimal("45.0"),
                module_angle=Decimal("30.0"),
                angle_unit=AngleUnit.DEG,
                primary_targeted_structure=CCFStructure.HPF,
                atlas_coordinates=[
                    Coordinate(
                        system_name="Bregma ARI",
                        position=[
                            FloatAxis(value=1.0, axis=AxisName.X),
                            FloatAxis(value=2.0, axis=AxisName.Y),
                            FloatAxis(value=3.0, axis=AxisName.Z),
                        ]
                    ),
                ],
                manipulator_coordinates=[
                    SurfaceCoordinate(
                        system_name="Bregma ARI",
                        position=[
                            FloatAxis(value=1.0, axis=AxisName.X),
                            FloatAxis(value=2.0, axis=AxisName.Y),
                            FloatAxis(value=3.0, axis=AxisName.Z),
                        ],
                        depth=1,
                    ),
                    SurfaceCoordinate(
                        system_name="Bregma ARI",
                        position=[
                            FloatAxis(value=4.0, axis=AxisName.X),
                            FloatAxis(value=5.0, axis=AxisName.Y),
                            FloatAxis(value=6.0, axis=AxisName.Z),
                        ],
                        depth=2,
                    ),
                ],
                manipulator_axis_positions=[
                    Coordinate(
                        system_name="Bregma ARI",
                        position=[
                            FloatAxis(value=1.0, axis=AxisName.X),
                            FloatAxis(value=2.0, axis=AxisName.Y),
                            FloatAxis(value=3.0, axis=AxisName.Z),
                        ]
                    ),
                    Coordinate(
                        system_name="Bregma ARI",
                        position=[
                            FloatAxis(value=4.0, axis=AxisName.X),
                            FloatAxis(value=5.0, axis=AxisName.Y),
                            FloatAxis(value=6.0, axis=AxisName.Z),
                        ]
                    ),
                ],
            )

        self.assertIn(
            "Length of atlas_coordinates, manipulator_coordinates, and manipulator_axis_positions must be the same",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
