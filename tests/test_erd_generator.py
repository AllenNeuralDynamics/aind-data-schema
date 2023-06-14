"""Unit test for erd_diagram_generator"""

import unittest
from unittest.mock import MagicMock, patch

from aind_data_schema.utils.erd_generator import ErdGenerator


class ErdGeneratorTests(unittest.TestCase):
    """Class for testing ErdGenerator"""

    @patch("erdantic.EntityRelationshipDiagram.draw")
    def test_classes_to_generate(self, mock_draw: MagicMock):
        """Tests that draw is called correctly"""

        erd = ErdGenerator(classes_to_generate=["Subject", "Processing"])
        erd.generate_erd_diagrams()
        assert mock_draw.call_count == len(erd.classes_to_generate)

    @patch("erdantic.EntityRelationshipDiagram.draw")
    def test_from_args(self, mock_draw: MagicMock):
        """Tests that class is constructed from args"""
        erd = ErdGenerator.from_args(["-c", "Subject", "Processing"])
        erd.generate_erd_diagrams()
        assert mock_draw.call_count == len(erd.classes_to_generate)


if __name__ == "__main__":
    unittest.main()
