"""Tests metadata module"""

import json
import re
import unittest
from datetime import time

from aind_data_schema_models.organizations import Organization
from aind_data_schema_models.platforms import Platform
from aind_data_schema_models.modalities import Modality
from pydantic import ValidationError
from pydantic import __version__ as pyd_version

from aind_data_schema.components.devices import MousePlatform
from aind_data_schema.core.acquisition import Acquisition
from aind_data_schema.core.data_description import DataDescription
from aind_data_schema.core.instrument import Instrument
from aind_data_schema.core.metadata import Metadata, MetadataStatus
from aind_data_schema.core.procedures import (
    IontophoresisInjection,
    NanojectInjection,
    Procedures,
    Surgery,
    ViralMaterial,
)
from aind_data_schema.core.processing import Processing
from aind_data_schema.core.rig import Rig
from aind_data_schema.core.session import Session
from aind_data_schema.core.subject import BreedingInfo, Sex, Species, Subject

PYD_VERSION = re.match(r"(\d+.\d+).\d+", pyd_version).group(1)


class TestMetadata(unittest.TestCase):
    """Class to test Metadata model"""

    def test_valid_subject_info(self):
        """Tests that the record is marked as VALID if a valid subject model
        is present."""
        s1 = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="123345",
            sex=Sex.MALE,
            date_of_birth="2020-10-10",
            source=Organization.AI,
            breeding_info=BreedingInfo(
                breeding_group="Emx1-IRES-Cre(ND)",
                maternal_id="546543",
                maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
                paternal_id="232323",
                paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
            ),
            genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)/wt",
        )
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=s1)
        self.assertEqual("ecephys_655019_2023-04-03_18-17-09", d1.name)
        self.assertEqual("bucket", d1.location)
        self.assertEqual(MetadataStatus.VALID, d1.metadata_status)
        self.assertEqual(s1, d1.subject)

    def test_missing_subject_info(self):
        """Marks the metadata status as MISSING if a Subject model is not
        present"""

        d1 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
        )
        self.assertEqual(MetadataStatus.MISSING, d1.metadata_status)
        self.assertEqual("ecephys_655019_2023-04-03_18-17-09", d1.name)
        self.assertEqual("bucket", d1.location)

        # Assert at least a name and location are required
        with self.assertRaises(ValidationError) as e:
            Metadata()
        expected_exception_message = (
            "2 validation errors for Metadata\n"
            "name\n"
            "  Field required [type=missing, input_value={}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing\n"
            "location\n"
            "  Field required [type=missing, input_value={}, input_type=dict]\n"
            f"    For further information visit https://errors.pydantic.dev/{PYD_VERSION}/v/missing"
        )
        self.assertEqual(expected_exception_message, str(e.exception))

    def test_invalid_core_models(self):
        """Test that invalid models don't raise an error, but marks the
        metadata_status as INVALID"""

        # Invalid subject model
        d1 = Metadata(name="ecephys_655019_2023-04-03_18-17-09", location="bucket", subject=Subject.model_construct())
        self.assertEqual(MetadataStatus.INVALID, d1.metadata_status)

        # Valid subject model, but invalid procedures model
        s2 = Subject(
            species=Species.MUS_MUSCULUS,
            subject_id="123345",
            sex=Sex.MALE,
            date_of_birth="2020-10-10",
            source=Organization.AI,
            breeding_info=BreedingInfo(
                breeding_group="Emx1-IRES-Cre(ND)",
                maternal_id="546543",
                maternal_genotype="Emx1-IRES-Cre/wt; Camk2a-tTa/Camk2a-tTA",
                paternal_id="232323",
                paternal_genotype="Ai93(TITL-GCaMP6f)/wt",
            ),
            genotype="Emx1-IRES-Cre;Camk2a-tTA;Ai93(TITL-GCaMP6f)/wt",
        )
        d2 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            subject=s2,
            procedures=Procedures.model_construct(injection_materials=["some materials"]),
        )
        self.assertEqual(MetadataStatus.INVALID, d2.metadata_status)

        # Tests constructed via dictionary
        d3 = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            subject=json.loads(Subject.model_construct().model_dump_json()),
        )
        self.assertEqual(MetadataStatus.INVALID, d3.metadata_status)

    def test_default_file_extension(self):
        """Tests that the default file extension used is as expected."""
        self.assertEqual(".nd.json", Metadata._FILE_EXTENSION.default)

    def test_validate_smartspim_metadata(self):
        """Tests that smartspim validator works as expected"""
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct()
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])

        # Tests missing metadata
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.SMARTSPIM,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.SPIM],
                ),
                procedures=Procedures.model_construct(subject_procedures=[surgery1]),
                acquisition=Acquisition.model_construct(),
            )
        self.assertIn(
            "SPIM metadata missing required file: subject",
            str(context.exception),
        )

        # Tests excluded metadata getting included
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.SMARTSPIM,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.SPIM],
                ),
                subject=Subject.model_construct(),
                session=Session.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery1]),
                acquisition=Acquisition.model_construct(),
            )
        self.assertIn(
            "SPIM metadata includes excluded file: session",
            str(context.exception),
        )

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.SMARTSPIM,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.SPIM],
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                acquisition=Acquisition.model_construct(),
                instrument=Instrument.model_construct(),
                processing=Processing.model_construct(),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_multi_modal_metadata(self):
        """Test that metadata with multiple modalities correctly prioritizes REQUIRED > OPTIONAL > EXCLUDED"""
        # Tests excluded metadata getting included
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct(injection_materials=[viral_material])
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])

        mouse_platform = MousePlatform.model_construct(name="platform1")
        rig = Rig.model_construct(rig_id="123_EPHYS1_20220101", mouse_platform=mouse_platform)
        session = Session.model_construct(rig_id="123_EPHYS1_20220101", mouse_platform_name="platform1")

        m = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            data_description=DataDescription.model_construct(
                label="some label",
                platform=Platform.SMARTSPIM,
                creation_time=time(12, 12, 12),
                modality=[Modality.BEHAVIOR, Modality.SPIM],  # technically this is impossible, but we need to test it
            ),
            subject=Subject.model_construct(),
            session=session,  # SPIM excludes session, but BEHAVIOR requires it
            procedures=Procedures.model_construct(subject_procedures=[surgery1]),
            acquisition=Acquisition.model_construct(),
            rig=rig,
            processing=Processing.model_construct(),
            instrument=Instrument.model_construct(),
        )
        self.assertIsNotNone(m)

    def test_validate_ecephys_metadata(self):
        """Tests that ecephys validator works as expected"""
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct()
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])

        # Tests missing metadata
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.ECEPHYS,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.ECEPHYS],
                ),
                procedures=Procedures.model_construct(subject_procedures=[surgery1]),
                rig=Rig.model_construct(),
            )
        self.assertIn(
            "ECEPHYS metadata missing required file: subject",
            str(context.exception),
        )

        # Tests missing injection materials
        surgery2 = Surgery.model_construct(procedures=[nano_inj])
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.ECEPHYS,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.ECEPHYS],
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(subject_procedures=[surgery2]),
                rig=Rig.model_construct(),
                processing=Processing.model_construct(),
                session=Session.model_construct(),
            )
        self.assertIn("Injection is missing injection_materials.", str(context.exception))

    def test_validate_underscore_modality(self):
        """Tests that ecephys validator works as expected"""
        viral_material = ViralMaterial.model_construct()
        nano_inj = NanojectInjection.model_construct(injection_materials=[viral_material])
        ionto_inj = IontophoresisInjection.model_construct(injection_materials=[viral_material])
        mouse_platform = MousePlatform.model_construct(name="platform1")
        rig = Rig.model_construct(rig_id="123_EPHYS2_20230101", mouse_platform=mouse_platform)
        session = Session.model_construct(rig_id="123_EPHYS2_20230101", mouse_platform_name="platform1")

        # Tests missing metadata
        surgery1 = Surgery.model_construct(procedures=[nano_inj, ionto_inj])
        m = Metadata(
            name="ecephys_655019_2023-04-03_18-17-09",
            location="bucket",
            data_description=DataDescription.model_construct(
                label="some label",
                platform=Platform.ECEPHYS,
                creation_time=time(12, 12, 12),
                modality=[Modality.BEHAVIOR_VIDEOS],
            ),
            subject=Subject.model_construct(),
            procedures=Procedures.model_construct(subject_procedures=[surgery1]),
            rig=rig,
            session=session,
        )
        self.assertIsNotNone(m)

    def test_validate_rig_session_compatibility(self):
        """Tests that rig/session compatibility validator works as expected"""
        mouse_platform = MousePlatform.model_construct(name="platform1")
        rig = Rig.model_construct(rig_id="123_EPHYS1_20220101", mouse_platform=mouse_platform)
        session = Session.model_construct(rig_id="123_EPHYS2_20230101", mouse_platform_name="platform2")
        with self.assertRaises(ValidationError) as context:
            Metadata(
                name="ecephys_655019_2023-04-03_18-17-09",
                location="bucket",
                data_description=DataDescription.model_construct(
                    label="some label",
                    platform=Platform.ECEPHYS,
                    creation_time=time(12, 12, 12),
                    modality=[Modality.ECEPHYS],
                ),
                subject=Subject.model_construct(),
                procedures=Procedures.model_construct(),
                rig=rig,
                processing=Processing.model_construct(),
                session=session,
            )
        self.assertIn(
            "Rig ID in session 123_EPHYS2_20230101 does not match the rig's 123_EPHYS1_20220101.",
            str(context.exception),
        )

    def test_validate_old_schema_version(self):
        """Tests that old schema versions are ignored during validation
        """
        m = Metadata.model_construct(
            name="name",
            location="location",
            id="1",
        )

        m_dict = m.model_dump()

        m_dict["schema_version"] = "0.0.0"
        m_dict.pop("id")

        m2 = Metadata(**m_dict)

        self.assertIsNotNone(m2)


if __name__ == "__main__":
    unittest.main()
