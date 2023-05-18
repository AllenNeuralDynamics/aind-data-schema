"""Unit test for erd_diagram_generator"""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from aind_data_schema.utils.erd_generator import ErdGenerator


class ErdGeneratorTests(unittest.TestCase):
    """Class for testing ErdGenerator"""

    @patch("erdantic.EntityRelationshipDiagram.draw")
    def test_classes_to_generate(self, mock_draw: MagicMock):
        """Tests that draw is called correctly"""

        erd = ErdGenerator(classes_to_generate=["Subject"])
        erd.generate_requested_classes()
        assert mock_draw.call_count == len(erd.classes_to_generate)

    @patch("erdantic.EntityRelationshipDiagram.draw")
    def test_generate_loaded_models(self, mock_draw: MagicMock):
        """Tests that draw is called correctly"""

        erd = ErdGenerator(classes_to_generate=[])
        erd.generate_aind_core_model_diagrams()
        assert mock_draw.call_count == len(erd.classes_to_generate)


if __name__ == "__main__":
    unittest.main()
