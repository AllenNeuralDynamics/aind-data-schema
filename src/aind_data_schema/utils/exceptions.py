"""Custom error codes for aind-data-schema"""

from typing import List


class FieldLengthMismatch(Exception):
    """Custom error for length mismatch in subfields of sectioning"""

    def __init__(self, class_name, fields: List[str]):
        message = f"Field length mismatch in {class_name}, excepted {fields} to be the same length."
        super().__init__(message)
        self.message = message
