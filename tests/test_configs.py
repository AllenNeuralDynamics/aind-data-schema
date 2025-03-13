""" Tests for the configs module """

import unittest
from decimal import Decimal
from pydantic import ValidationError
from aind_data_schema.components.configs import MRIScan, Rotation, Translation, Scale, ManipulatorConfig
from aind_data_schema.components.coordinates import FloatAxis, AxisName, Coordinate
from aind_data_schema_models.brain_atlas import CCFStructure


class TestMRIScan(unittest.TestCase):
    """Tests for the MRIScan class"""

    def test_validate_primary_scan_success(self):
        """Test validate_primary_scan method with valid primary scan data"""
        valid_data = {
            "device_name": "MRI Scanner",
            "scan_index": 1,
            "scan_type": "3D Scan",
            "primary_scan": True,
            "scan_sequence_type": "RARE",
            "echo_time": Decimal("10.0"),
            "repetition_time": Decimal("2000.0"),
            "subject_position": "Prone",
            "additional_scan_parameters": {},
            "vc_orientation": Rotation(
                angles=[
                    FloatAxis(value=1.0, axis=AxisName.ML),
                    FloatAxis(value=1.0, axis=AxisName.SI),
                    FloatAxis(value=1.0, axis=AxisName.AP),
                ],
                order=[AxisName.AP, AxisName.SI, AxisName.ML],
            ),
            "vc_position": Translation(
                translation=[
                    FloatAxis(value=1.0, axis=AxisName.ML),
                    FloatAxis(value=1.0, axis=AxisName.SI),
                    FloatAxis(value=1.0, axis=AxisName.AP),
                ]
            ),
            "voxel_sizes": Scale(
                scale=[
                    FloatAxis(value=0.5, axis=AxisName.AP),
                    FloatAxis(value=0.4375, axis=AxisName.ML),
                    FloatAxis(value=0.52, axis=AxisName.SI),
                ]
            ),
        }
        scan = MRIScan(**valid_data)
        self.assertTrue(scan.primary_scan)

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
            position=[
                FloatAxis(value=1.0, axis=AxisName.X),
                FloatAxis(value=2.0, axis=AxisName.Y),
                FloatAxis(value=3.0, axis=AxisName.Z),
            ]
        )
        coordinate2 = Coordinate(
            position=[
                FloatAxis(value=4.0, axis=AxisName.X),
                FloatAxis(value=5.0, axis=AxisName.Y),
                FloatAxis(value=6.0, axis=AxisName.Z),
            ]
        )
        config = ManipulatorConfig(
            device_name="Manipulator",
            arc_angle=Decimal("45.0"),
            module_angle=Decimal("30.0"),
            angle_unit="deg",
            primary_targeted_structure=CCFStructure.HPF,
            atlas_coordinates=[coordinate1, coordinate2],
            manipulator_coordinates=[coordinate1, coordinate2],
            manipulator_axis_positions=[coordinate1, coordinate2],
        )
        self.assertIsInstance(config, ManipulatorConfig)

    def test_validate_len_coordinates_failure(self):
        """Test validate_len_coordinates method with invalid coordinate lengths"""
        invalid_data = {
            "device_name": "Manipulator",
            "arc_angle": Decimal("45.0"),
            "module_angle": Decimal("30.0"),
            "angle_unit": "deg",
            "primary_targeted_structure": "SomeStructure",
            "atlas_coordinates": [
                Coordinate(
                    position=[
                        FloatAxis(value=1.0, axis=AxisName.X),
                        FloatAxis(value=2.0, axis=AxisName.Y),
                        FloatAxis(value=3.0, axis=AxisName.Z),
                    ]
                ),
            ],
            "manipulator_coordinates": [
                Coordinate(
                    position=[
                        FloatAxis(value=1.0, axis=AxisName.X),
                        FloatAxis(value=2.0, axis=AxisName.Y),
                        FloatAxis(value=3.0, axis=AxisName.Z),
                    ]
                ),
                Coordinate(
                    position=[
                        FloatAxis(value=4.0, axis=AxisName.X),
                        FloatAxis(value=5.0, axis=AxisName.Y),
                        FloatAxis(value=6.0, axis=AxisName.Z),
                    ]
                ),
            ],
            "manipulator_axis_positions": [
                Coordinate(
                    position=[
                        FloatAxis(value=1.0, axis=AxisName.X),
                        FloatAxis(value=2.0, axis=AxisName.Y),
                        FloatAxis(value=3.0, axis=AxisName.Z),
                    ]
                ),
                Coordinate(
                    position=[
                        FloatAxis(value=4.0, axis=AxisName.X),
                        FloatAxis(value=5.0, axis=AxisName.Y),
                        FloatAxis(value=6.0, axis=AxisName.Z),
                    ]
                ),
            ],
        }
        with self.assertRaises(ValueError):
            ManipulatorConfig(**invalid_data)


if __name__ == "__main__":
    unittest.main()
