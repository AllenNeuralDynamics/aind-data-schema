""" Tests for the configs module """

import unittest
from decimal import Decimal
from pydantic import ValidationError
from aind_data_schema.components.configs import MRIScan, Rotation, Translation, Scale
from aind_data_schema.components.coordinates import FloatAxis, AxisName


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
                    FloatAxis(value=1.0, axis=AxisName.DV),
                    FloatAxis(value=1.0, axis=AxisName.AP),
                ],
                order=[AxisName.AP, AxisName.DV, AxisName.ML],
            ),
            "vc_position": Translation(
                translation=[
                    FloatAxis(value=1.0, axis=AxisName.ML),
                    FloatAxis(value=1.0, axis=AxisName.DV),
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


if __name__ == "__main__":
    unittest.main()
