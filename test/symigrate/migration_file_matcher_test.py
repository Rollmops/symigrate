import unittest

from symigrate.migration_file_matcher import MigrationFileMatcher


class MigrationFileMatcherTestCase(unittest.TestCase):
    def test_match(self):
        migration_file_matcher = MigrationFileMatcher("V", "__", ".sh")

        match = migration_file_matcher.match("V1.2.3__some_description.sh")

        self.assertIsNotNone(match)
        self.assertEqual("1.2.3", match.version)
        self.assertEqual("some description", match.description)

    def test_should_not_match(self):
        migration_file_matcher = MigrationFileMatcher("V", "__", ".sh")

        match = migration_file_matcher.match("V1.2.3__some_description_sh")

        self.assertIsNone(match)
