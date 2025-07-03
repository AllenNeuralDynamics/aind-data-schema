"""Tests for CalibrationFit from measurements module"""

import unittest
from pydantic import ValidationError
from aind_data_schema.components.measurements import CalibrationFit, FitType


class TestCalibrationFit(unittest.TestCase):
    """Tests for CalibrationFit class"""

    def test_linear_interpolation_without_parameters(self):
        """Test that linear interpolation fit type works without parameters"""
        fit = CalibrationFit(fit_type=FitType.LINEAR_INTERPOLATION)
        self.assertEqual(fit.fit_type, FitType.LINEAR_INTERPOLATION.value)
        self.assertIsNone(fit.fit_parameters)

    def test_linear_interpolation_with_parameters_raises_error(self):
        """Test that linear interpolation fit type raises error with parameters"""
        with self.assertRaises(ValidationError) as context:
            CalibrationFit(fit_type=FitType.LINEAR_INTERPOLATION, fit_parameters={"slope": 1.0, "intercept": 0.0})
        self.assertIn("Fit parameters should not be provided for linear interpolation fit type", str(context.exception))

    def test_linear_fit_with_parameters(self):
        """Test that linear fit type works with parameters"""
        parameters = {"slope": 1.5, "intercept": 2.0}
        fit = CalibrationFit(fit_type=FitType.LINEAR, fit_parameters=parameters)
        self.assertEqual(fit.fit_type, FitType.LINEAR.value)
        # Compare the fit_parameters as a dict using model_dump()
        self.assertIsNotNone(fit.fit_parameters)
        self.assertEqual(fit.fit_parameters.model_dump(), parameters)

    def test_linear_fit_without_parameters_raises_error(self):
        """Test that linear fit type raises error without parameters"""
        with self.assertRaises(ValidationError) as context:
            CalibrationFit(fit_type=FitType.LINEAR)
        self.assertIn("Fit parameters must be provided for linear fit type", str(context.exception))

    def test_other_fit_with_parameters(self):
        """Test that other fit type works with parameters"""
        parameters = {"a": 1.0, "b": 2.0, "c": 3.0}
        fit = CalibrationFit(fit_type=FitType.OTHER, fit_parameters=parameters)
        self.assertEqual(fit.fit_type, FitType.OTHER.value)
        # Compare the fit_parameters as a dict using model_dump()
        self.assertIsNotNone(fit.fit_parameters)
        self.assertEqual(fit.fit_parameters.model_dump(), parameters)

    def test_other_fit_without_parameters_raises_error(self):
        """Test that other fit type raises error without parameters"""
        with self.assertRaises(ValidationError) as context:
            CalibrationFit(fit_type=FitType.OTHER)
        self.assertIn("Fit parameters must be provided for other fit type", str(context.exception))

    def test_linear_fit_with_none_parameters_raises_error(self):
        """Test that linear fit type raises error with None parameters"""
        with self.assertRaises(ValidationError) as context:
            CalibrationFit(fit_type=FitType.LINEAR, fit_parameters=None)
        self.assertIn("Fit parameters must be provided for linear fit type", str(context.exception))

    def test_other_fit_with_none_parameters_raises_error(self):
        """Test that other fit type raises error with None parameters"""
        with self.assertRaises(ValidationError) as context:
            CalibrationFit(fit_type=FitType.OTHER, fit_parameters=None)
        self.assertIn("Fit parameters must be provided for other fit type", str(context.exception))


if __name__ == "__main__":
    unittest.main()
