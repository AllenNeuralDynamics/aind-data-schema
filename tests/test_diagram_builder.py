"""Tests diagrams module"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from aind_data_schema.core.subject import Subject
from aind_data_schema.utils.diagrams import save_all_core_model_diagrams, save_diagram


class DiagramBuilderTests(unittest.TestCase):
    """Tests for DiagramBuilder methods"""

    @patch("erdantic.erd.EntityRelationshipDiagram.draw")
    def test_save_diagram_default(self, mock_draw: MagicMock):
        """Tests save_diagram_default method"""
        save_diagram(Subject)

        mock_draw.assert_called_once_with(Path("Subject.svg"))

    @patch("erdantic.erd.EntityRelationshipDiagram.draw")
    def test_save_diagram_dir(self, mock_draw: MagicMock):
        """Tests save_diagram_default method with output_directory"""
        save_diagram(model=Subject, output_directory=Path("some_dir"))

        mock_draw.assert_called_once_with(Path("some_dir") / "Subject.svg")

    @patch("erdantic.erd.EntityRelationshipDiagram.draw")
    def test_save_diagram_dir_and_filename(self, mock_draw: MagicMock):
        """Tests save_diagram_default method with output_directory and filename"""
        save_diagram(model=Subject, output_directory=Path("some_dir"), filename="subject_a.svg")

        mock_draw.assert_called_once_with(Path("some_dir") / "subject_a.svg")

    @patch("erdantic.erd.EntityRelationshipDiagram.draw")
    def test_save_all_core_diagrams_default(self, mock_draw: MagicMock):
        """Tests save_all_core_diagrams_default method"""
        save_all_core_model_diagrams()

        mock_draw.assert_has_calls(
            [
                call(Path("subject.svg")),
                call(Path("processing.svg")),
                call(Path("data_description.svg")),
                call(Path("acquisition.svg")),
                call(Path("instrument.svg")),
                call(Path("procedures.svg")),
                call(Path("rig.svg")),
                call(Path("session.svg")),
                call(Path("metadata.nd.svg")),
            ],
            any_order=True,
        )

    @patch("erdantic.erd.EntityRelationshipDiagram.draw")
    def test_save_all_core_diagrams_dir(self, mock_draw: MagicMock):
        """Tests save_all_core_diagrams_default method with output_directory"""
        save_all_core_model_diagrams(output_directory=Path("some_dir"))

        mock_draw.assert_has_calls(
            [
                call(Path("some_dir") / "subject.svg"),
                call(Path("some_dir") / "processing.svg"),
                call(Path("some_dir") / "data_description.svg"),
                call(Path("some_dir") / "acquisition.svg"),
                call(Path("some_dir") / "instrument.svg"),
                call(Path("some_dir") / "procedures.svg"),
                call(Path("some_dir") / "rig.svg"),
                call(Path("some_dir") / "session.svg"),
                call(Path("some_dir") / "metadata.nd.svg"),
            ],
            any_order=True,
        )


if __name__ == "__main__":
    unittest.main()
