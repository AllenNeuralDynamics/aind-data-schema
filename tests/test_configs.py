import unittest
from decimal import Decimal
from pydantic import ValidationError
from aind_data_schema.components.configs import MRIScan, Rotation3dTransform, Translation3dTransform, Scale3dTransform, SubjectPosition, MriScanSequence, ProcessName, TimeUnit


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
            "vc_orientation": Rotation3dTransform(rotation=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            "vc_position": Translation3dTransform(translation=[0.0, 0.0, 0.0]),
            "voxel_sizes": Scale3dTransform(scale=[1.0, 1.0, 1.0]),
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
