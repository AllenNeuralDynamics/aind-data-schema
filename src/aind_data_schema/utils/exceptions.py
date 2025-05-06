"""Custom error codes for aind-data-schema"""

from typing import List


class OneOfError(Exception):
    """Custom error when one of a list of fields is required"""

    def __init__(self, class_name, fields: List[str]):
        """Init"""
        message = f"Error in {class_name} one of the fields {fields} is required."
        super().__init__(message)
        self.message = message
