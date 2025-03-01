"""Tests acquisition validators in Metadata model"""

import unittest
from datetime import datetime, time, timezone

from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization
from pydantic import ValidationError

from aind_data_schema.components.devices import (
    EphysAssembly,
    EphysProbe,
    Manipulator,
    MousePlatform,
)
from aind_data_schema.core.acquisition import Acquisition, SubjectDetails, DataStream

from aind_data_schema.core.instrument import Instrument
from aind_data_schema.components.configs import DomeModule
from aind_data_schema.core.metadata import Metadata
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.procedures import Procedures
from aind_data_schema.core.subject import Subject
from aind_data_schema.core.data_description import DataDescription


ephys_assembly = EphysAssembly(
    probes=[EphysProbe(probe_model="Neuropixels 1.0", name="Probe A")],
    manipulator=Manipulator(
        name="Probe manipulator",
        manufacturer=Organization.NEW_SCALE_TECHNOLOGIES,
        serial_number="4321",
    ),
    name="Ephys_assemblyA",
)


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    def test_validate_acquisition_modality_requirements(self):
        """Tests that the acquisition modality requirements validator works as expected"""
        modalities = [Modality.ECEPHYS]
        mouse_platform = MousePlatform.model_construct(name="platform1")
        inst = Instrument.model_construct(
            instrument_id="123_EPHYS1_20220101",
            modalities=modalities,
            components=[ephys_assembly, mouse_platform],
        )
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=time(12, 12, 12),
                    modalities=modalities,
                    subject_id="655019",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(),
                instrument=inst,
                processing=Processing.model_construct(),
                acquisition=Acquisition.model_construct(
                    instrument_id="123_EPHYS1_20220101",
                    data_streams=[
                        DataStream(
                            stream_start_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
                            stream_end_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
                            active_devices=[],
                            configurations=[],
                            modalities=[Modality.BEHAVIOR_VIDEOS],
                        ),
                    ],
                    subject_details=SubjectDetails.model_construct(mouse_platform_name="platform1"),
                ),
            )
        self.assertIn(
            "Modality 'behavior-videos' requires one of",
            str(context.exception),
        )

    def test_validate_acquisition_config_requirements(self):
        """Tests that the acquisition config requirements validator works as expected"""

        # Warning if we ever add a requirement for confocal this Instrument will stop being valid
        modalities = [Modality.CONFOCAL]
        inst = Instrument.model_construct(
            instrument_id="123_EPHYS1_20220101",
            modalities=modalities,
            components=[],
        )
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="655019_2023-04-03T181709",
                location="bucket",
                data_description=DataDescription.model_construct(
                    creation_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
                    modalities=modalities,
                    subject_id="655019",
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(),
                instrument=inst,
                processing=Processing.model_construct(),
                acquisition=Acquisition.model_construct(
                    instrument_id="123_EPHYS1_20220101",
                    data_streams=[
                        DataStream(
                            stream_start_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
                            stream_end_time=datetime(2022, 11, 22, 8, 43, 00, tzinfo=timezone.utc),
                            modalities=[Modality.ECEPHYS],
                            active_devices=[],
                            configurations=[DomeModule.model_construct()],
                        ),
                    ],
                    subject_details=SubjectDetails.model_construct(mouse_platform_name="platform1"),
                ),
            )
        self.assertIn(
            "Configuration 'DomeModule' requires one of",
            str(context.exception),
        )


if __name__ == "__main__":
    unittest.main()
