"""Test identifier module"""

import unittest

from pydantic import ValidationError

from aind_data_schema.components.identifiers import Code, DataAsset, Person


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
            ("a" * 60, "a" * 60),
            ("aBcDeF1", "aBcDeF1"),
            ("deadbeef1234", "deadbeef1234"),
            ("  abc1234  ", "abc1234"),  # strip_whitespace=True strips before validation
        ]
        for git_hash, expected in cases:
            with self.subTest(git_hash=git_hash):
                code = Code(url="https://github.com/org/repo", commit_hash=git_hash)
                self.assertEqual(code.commit_hash, expected)

    def test_git_hash_invalid(self):
        """Invalid git hashes raise ValidationError"""
        cases = [
            "abc123",  # too short (6 chars)
            "a" * 61,  # too long (61 chars)
            "xyz12345",  # non-hex characters
        ]
        for git_hash in cases:
            with self.subTest(git_hash=git_hash):
                with self.assertRaises(ValidationError):
                    Code(url="https://github.com/org/repo", commit_hash=git_hash)


class TestDataAsset(unittest.TestCase):
    """Test DataAsset validator"""

    def test_name_provided_directly(self):
        """Name is kept as-is when explicitly provided"""
        asset = DataAsset(name="my-dataset")
        self.assertEqual(asset.name, "my-dataset")

    def test_name_parsed_from_url_no_subpath(self):
        """Name is inferred from top-level prefix with no nested path"""
        asset = DataAsset(url="s3://aind-open-data/my-dataset")
        self.assertEqual(asset.name, "my-dataset")

    def test_name_parsed_from_url_with_subpath(self):
        """Name is inferred from top-level prefix, ignoring nested path"""
        asset = DataAsset(url="s3://aind-open-data/my-dataset/sub/path/file.txt")
        self.assertEqual(asset.name, "my-dataset")

    def test_name_not_overridden_when_provided_with_url(self):
        """Explicit name takes precedence over URL-inferred name"""
        asset = DataAsset(name="explicit-name", url="s3://aind-open-data/other-dataset/sub")
        self.assertEqual(asset.name, "explicit-name")

    def test_neither_name_nor_url_raises(self):
        """Raises ValidationError when neither name nor url is provided"""
        with self.assertRaises(ValidationError):
            DataAsset()

    def test_url_wrong_bucket_leaves_name_none(self):
        """URL from a different bucket does not set name (remains None)"""
        asset = DataAsset(url="s3://other-bucket/my-dataset")
        self.assertIsNone(asset.name)


if __name__ == "__main__":
    unittest.main()
