import unittest

from pydantic import BaseModel, Field
from aind_data_schema.core.quality_control import QualityControl


class ExtensionTests(unittest.TestCase):
    """tests for examples"""

    def test_extension(self):
        """run through each example, compare to rendered json"""

        class QCExtension(BaseModel):
            """Extension for QualityControl"""

            example: str = Field(..., title="Example")

        qcext = QCExtension(example="example")

        qc = QualityControl(
            evaluations = [],
            extensions=qcext
        )
