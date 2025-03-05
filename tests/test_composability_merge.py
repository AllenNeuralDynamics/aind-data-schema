""" Test for merge functions """

import unittest
from datetime import datetime, timezone, date

from aind_data_schema.core.quality_control import QualityControl, QCEvaluation, QCMetric, QCStatus, Status, Stage

from aind_data_schema.core.acquisition import Acquisition, DataStream, SubjectDetails
from aind_data_schema.core.procedures import Procedures, Reagent, Surgery, Anaesthetic, Craniotomy, Perfusion
from aind_data_schema.core.processing import Processing, DataProcess, ProcessName, ProcessStage
from aind_data_schema.components.identifiers import Person, Code
from aind_data_schema.components.configs import InVitroImagingConfig, Immersion
from aind_data_schema.components.coordinates import ImageAxis, Scale3dTransform, Translation3dTransform
from aind_data_schema.components.devices import Calibration, Maintenance

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.pid_names import PIDName
from aind_data_schema_models.registries import Registry
from aind_data_schema_models.units import PowerUnit
from aind_data_schema_models.modalities import Modality

from aind_data_schema.components import tile


class TestComposability(unittest.TestCase):
    """Tests for merge functions"""

    def test_merge_quality_control(self):
        """Test adding two QualityControl objects"""

        test_eval = QCEvaluation(
            name="Drift map",
            modality=Modality.ECEPHYS,
            stage=Stage.PROCESSING,
            metrics=[
                QCMetric(
                    name="Dict example",
                    value={"stuff": "in_a_dict"},
                    status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
                QCMetric(
                    name="Drift map pass/fail",
                    value=False,
                    description="Manual evaluation of whether the drift map looks good",
                    reference="s3://some-data-somewhere",
                    status_history=[
                        QCStatus(evaluator="Bob", timestamp=datetime.fromisoformat("2020-10-10"), status=Status.PASS)
                    ],
                ),
            ],
        )

        q1 = QualityControl(
            evaluations=[test_eval, test_eval],
        )

        q2 = QualityControl(
            evaluations=[test_eval],
        )

        q3 = q1 + q2
        self.assertIsNotNone(q3)
        self.assertTrue(len(q3.evaluations) == 3)

        # Test incompatible schema versions
        q1_orig_schema_v = q1.schema_version
        q1.schema_version = "0.1.0"

        with self.assertRaises(ValueError) as context:
            q1 + q2
        self.assertTrue(
            "Cannot combine QualityControl objects with different schema versions" in repr(context.exception)
        )

        # Test various versions of concatenating notes
        q1.schema_version = q1_orig_schema_v
        q1.notes = "note1"
        q2.notes = "note2"
        q3 = q1 + q2
        self.assertTrue(q3.notes == "note1\nnote2")

        q1.notes = None
        q3 = q1 + q2
        self.assertTrue(q3.notes == "note2")

        q1.notes = "note1"
        q2.notes = None
        q3 = q1 + q2
        self.assertTrue(q3.notes == "note1")

    def test_merge_acquisition(self):
        """Test merging two Acquisition objects"""

        t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

        acq1 = Acquisition(
            experimenters=[Person(name="John Smith")],
            specimen_id="###",
            subject_id="###",
            instrument_id="###",
            maintenance=[
                Maintenance(
                    maintenance_date=t,
                    device_name="Chamber",
                    description="Clean chamber",
                    reagents=[
                        Reagent(
                            name="reagent1",
                            source=Organization.OTHER,
                            rrid=PIDName(
                                name="xxx", abbreviation="xx", registry=Registry.RRID, registry_identifier="100"
                            ),
                            lot_number="xxx",
                            expiration_date=t.date(),
                        ),
                    ],
                )
            ],
            calibrations=[
                Calibration(
                    calibration_date=t,
                    device_name="Laser_1",
                    description="Laser power calibration",
                    input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
                    output={
                        "power_measurement": 50.0,
                        "power_unit": PowerUnit.MW,
                    },
                )
            ],
            data_streams=[
                DataStream(
                    stream_start_time=t,
                    stream_end_time=t,
                    modalities=[Modality.SPIM],
                    active_devices=[],
                    configurations=[
                        InVitroImagingConfig(
                            chamber_immersion=Immersion(
                                medium="PBS",
                                refractive_index=1.33,
                            ),
                            axes=[
                                ImageAxis(
                                    name="X",
                                    dimension=2,
                                    direction="Left_to_right",
                                ),
                                ImageAxis(
                                    name="Y",
                                    dimension=1,
                                    direction="Anterior_to_posterior",
                                ),
                                ImageAxis(
                                    name="Z",
                                    dimension=0,
                                    direction="Inferior_to_superior",
                                ),
                            ],
                            tiles=[
                                tile.AcquisitionTile(
                                    file_name="tile_X_0000_Y_0000_Z_0000_CH_488.ims",
                                    coordinate_transformations=[
                                        Scale3dTransform(scale=[0.748, 0.748, 1]),
                                        Translation3dTransform(translation=[0, 0, 0]),
                                    ],
                                    channel=tile.Channel(
                                        channel_name="488",
                                        excitation_wavelength=488,
                                        excitation_power=200,
                                        light_source_name="Ex_488",
                                        filter_names=["Em_600"],
                                        detector_name="PMT_1",
                                        filter_wheel_index=0,
                                    ),
                                    notes="these are my notes",
                                ),
                            ],
                        ),
                    ],
                )
            ],
            acquisition_start_time=t,
            acquisition_end_time=t,
            experiment_type="ExaSPIM",
        )

        acq2 = Acquisition(
            experimenters=[Person(name="Jane Doe")],
            specimen_id="###",
            subject_id="###",
            instrument_id="###",
            maintenance=[
                Maintenance(
                    maintenance_date=t,
                    device_name="Chamber",
                    description="Clean chamber",
                    reagents=[
                        Reagent(
                            name="reagent2",
                            source=Organization.OTHER,
                            rrid=PIDName(
                                name="yyy", abbreviation="yy", registry=Registry.RRID, registry_identifier="200"
                            ),
                            lot_number="yyy",
                            expiration_date=t.date(),
                        ),
                    ],
                )
            ],
            calibrations=[
                Calibration(
                    calibration_date=t,
                    device_name="Laser_2",
                    description="Laser power calibration",
                    input={"power_setting": 100.0, "power_unit": PowerUnit.PERCENT},
                    output={
                        "power_measurement": 60.0,
                        "power_unit": PowerUnit.MW,
                    },
                )
            ],
            data_streams=[
                DataStream(
                    stream_start_time=t,
                    stream_end_time=t,
                    modalities=[Modality.SPIM],
                    active_devices=[],
                    configurations=[
                        InVitroImagingConfig(
                            chamber_immersion=Immersion(
                                medium="PBS",
                                refractive_index=1.33,
                            ),
                            axes=[
                                ImageAxis(
                                    name="X",
                                    dimension=2,
                                    direction="Left_to_right",
                                ),
                                ImageAxis(
                                    name="Y",
                                    dimension=1,
                                    direction="Anterior_to_posterior",
                                ),
                                ImageAxis(
                                    name="Z",
                                    dimension=0,
                                    direction="Inferior_to_superior",
                                ),
                            ],
                            tiles=[
                                tile.AcquisitionTile(
                                    file_name="tile_X_0000_Y_0000_Z_0000_CH_561.ims",
                                    coordinate_transformations=[
                                        Scale3dTransform(scale=[0.748, 0.748, 1]),
                                        Translation3dTransform(translation=[0, 0, 0]),
                                    ],
                                    channel=tile.Channel(
                                        channel_name="561",
                                        excitation_wavelength=561,
                                        excitation_power=200,
                                        light_source_name="Ex_561",
                                        filter_names=["Em_600"],
                                        detector_name="PMT_1",
                                        filter_wheel_index=0,
                                    ),
                                    notes="these are my notes",
                                ),
                            ],
                        ),
                    ],
                )
            ],
            acquisition_start_time=t,
            acquisition_end_time=t,
            experiment_type="ExaSPIM",
        )

        merged_acq = acq1 + acq2

        self.assertEqual(len(merged_acq.experimenters), 2)
        self.assertEqual(len(merged_acq.maintenance), 2)
        self.assertEqual(len(merged_acq.calibrations), 2)
        self.assertEqual(len(merged_acq.data_streams), 2)
        self.assertEqual(merged_acq.acquisition_start_time, t)
        self.assertEqual(merged_acq.acquisition_end_time, t)
        self.assertEqual(merged_acq.experiment_type, "ExaSPIM")

        # Test incompatible schema versions
        acq1_orig_schema_v = acq1.schema_version
        acq1.schema_version = "0.1.0"

        with self.assertRaises(ValueError) as context:
            acq1 + acq2
        self.assertTrue("Cannot combine Acquisition objects with different schema versions" in repr(context.exception))

        acq1.schema_version = acq1_orig_schema_v

        # Test incompatible subject IDs
        acq2.subject_id = "different_id"
        with self.assertRaises(ValueError) as context:
            acq1 + acq2
        self.assertTrue("Cannot combine Acquisition objects that differ in key fields" in repr(context.exception))

        # Test incompatible SubjectDetails
        acq2.subject_id = acq1.subject_id
        subject_details = SubjectDetails(
            mouse_platform_name="mouse_platform_name",
        )
        acq1.subject_details = subject_details
        acq2.subject_details = subject_details

        with self.assertRaises(ValueError) as context:
            acq1 + acq2
        self.assertTrue("SubjectDetails cannot be combined in Acquisition" in repr(context.exception))

    def test_procedures_add(self):
        """Test the __add__ method of Procedures"""

        t = date(2022, 7, 12)
        t2 = date(2022, 9, 23)

        p1 = Procedures(
            subject_id="625100",
            subject_procedures=[
                Surgery(
                    start_date=t,
                    protocol_id="doi",
                    experimenters=[Person(name="Scientist Smith")],
                    ethics_review_id="2109",
                    animal_weight_prior=22.6,
                    animal_weight_post=22.3,
                    anaesthesia=Anaesthetic(type="Isoflurane", duration=1, level=1.5),
                    workstation_id="SWS 3",
                    procedures=[
                        Craniotomy(
                            craniotomy_type="Visual Cortex",
                            protocol_id="1234",
                            craniotomy_hemisphere="Left",
                            bregma_to_lambda_distance=4.1,
                        )
                    ],
                )
            ],
        )

        p2 = Procedures(
            subject_id="625100",
            subject_procedures=[
                Surgery(
                    start_date=t2,
                    protocol_id="doi",
                    experimenters=[Person(name="Scientist Smith")],
                    ethics_review_id="2109",
                    procedures=[
                        Perfusion(
                            protocol_id="doi_of_protocol",
                            output_specimen_ids=["2", "1"],
                        )
                    ],
                )
            ],
        )

        combined = p1 + p2

        self.assertEqual(combined.subject_id, "625100")
        self.assertEqual(len(combined.subject_procedures), 2)
        self.assertEqual(combined.subject_procedures[0].start_date, t)
        self.assertEqual(combined.subject_procedures[1].start_date, t2)

        # Test combining with different subject IDs raises ValueError
        p3 = Procedures(subject_id="different_id")
        with self.assertRaises(ValueError):
            _ = p1 + p3

        p2.schema_version = "0.0.0"
        with self.assertRaises(ValueError) as context:
            _ = p1 + p2

        self.assertIn("Schema versions must match to combine Procedures", str(context.exception))

    def test_add_processing_objects(self):
        """Test the __add__ method of Processing"""

        t = datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc)

        # Create two simple Processing objects
        p1 = Processing(
            data_processes=[
                DataProcess(
                    experimenters=[Person(name="Dr. Dan")],
                    name=ProcessName.ANALYSIS,
                    stage=ProcessStage.PROCESSING,
                    input_location="/path/to/inputs1",
                    output_location="/path/to/outputs1",
                    start_date_time=t,
                    end_date_time=t,
                    code=Code(
                        url="https://url/for/analysis1",
                        version="0.1.1",
                    ),
                ),
            ],
            notes="First processing object",
        )

        p2 = Processing(
            data_processes=[
                DataProcess(
                    experimenters=[Person(name="Dr. Jane")],
                    name=ProcessName.COMPRESSION,
                    stage=ProcessStage.PROCESSING,
                    input_location="/path/to/inputs2",
                    output_location="/path/to/outputs2",
                    start_date_time=t,
                    end_date_time=t,
                    code=Code(
                        url="https://url/for/compression",
                        version="0.1.1",
                    ),
                ),
            ],
            notes="Second processing object",
        )

        # Combine the two Processing objects
        combined = p1 + p2

        # Check that the combined object has the correct data_processes and notes
        self.assertEqual(len(combined.data_processes), 2)
        self.assertEqual(combined.data_processes[0].name, ProcessName.ANALYSIS)
        self.assertEqual(combined.data_processes[1].name, ProcessName.COMPRESSION)
        self.assertIn("First processing object", combined.notes)
        self.assertIn("Second processing object", combined.notes)

        # Test with incompatible schema versions
        p3 = p2
        p3.schema_version = "0.0.0"

        with self.assertRaises(ValueError) as e:
            _ = p1 + p3
        self.assertIn("Cannot add Processing objects with different schema versions.", str(e.exception))


if __name__ == "__main__":
    unittest.main()
