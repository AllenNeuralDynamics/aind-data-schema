"""Test identifier module"""

import unittest

from pydantic import ValidationError

from aind_data_schema.components.identifiers import Code, Person


class Testexperimenter(unittest.TestCase):
    """Test experimenter class"""

    def test_experimenter_with_full_name(self):
        """Test experimenter with first and last name"""
        experimenter = Person(name="John Doe", registry_identifier="0000-0001-2345-6789")
        self.assertIsNotNone(experimenter)
        self.assertEqual(experimenter.name, "John Doe")
        self.assertEqual(experimenter.registry_identifier, "0000-0001-2345-6789")

    def test_experimenter_missing_fields(self):
        """Test experimenter missing required fields"""
        with self.assertRaises(ValidationError):
            Person()


class TestGitHash(unittest.TestCase):
    """Test GitHash type validation via Code model"""

    def test_git_hash_valid(self):
        """Valid git hashes are accepted and stored correctly"""
        cases = [
            ("abc1234", "abc1234"),
            ("a" * 40, "a" * 40),
            ("aBcDeF1", "aBcDeF1"),
            ("deadbeef1234", "deadbeef1234"),
            ("  abc1234  ", "abc1234"),  # strip_whitespace=True strips before validation
        ]
        for git_hash, expected in cases:
            with self.subTest(git_hash=git_hash):
                code = Code(url="https://github.com/org/repo", git_hash=git_hash)
                self.assertEqual(code.git_hash, expected)

    def test_git_hash_invalid(self):
        """Invalid git hashes raise ValidationError"""
        cases = [
            "abc123",  # too short (6 chars)
            "a" * 41,  # too long (41 chars)
            "xyz12345",  # non-hex characters
        ]
        for git_hash in cases:
            with self.subTest(git_hash=git_hash):
                with self.assertRaises(ValidationError):
                    Code(url="https://github.com/org/repo", git_hash=git_hash)


if __name__ == "__main__":
    unittest.main()
