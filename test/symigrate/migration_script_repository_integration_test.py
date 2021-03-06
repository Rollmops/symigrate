import os
import unittest

from symigrate.migration_file_matcher import MigrationFileMatcher
from symigrate.repository.migration_script_repository import MigrationScriptRepository


class MigrationRepositoryIntegrationTestCase(unittest.TestCase):

    def setUp(self):
        test_data_directory_path = os.path.join(os.path.dirname(__file__), "data", "migrations")
        self.assertTrue(os.path.isdir(test_data_directory_path))

        migration_file_matcher = MigrationFileMatcher("V", "__", ".sh")
        self.migration_repository = MigrationScriptRepository(
            test_data_directory_path,
            "DEFAULT",
            "utf-8",
            migration_file_matcher
        )

    def test_find_all(self):
        migrations = self.migration_repository.find_all()

        self.assertEqual(2, len(migrations))

        self.assertEqual("1.0.0", migrations[0].version)
        self.assertEqual("1.1.0", migrations[1].version)

        self.assertEqual("test migration", migrations[0].description)
        self.assertEqual("another migration", migrations[1].description)

        self.assertEqual("229175e221c1afad4c436279e1ebc54c", migrations[0].checksum)
        self.assertEqual("cc75a79b4c7c66943fcd3651cd8ace9b", migrations[1].checksum)

        expected_content_1 = """#!/usr/bin/env bash

echo "Hello, World from 1.0.0"
"""
        expected_content_2 = """#!/usr/bin/env bash

echo "Hello from 1.1.0"
"""
        self.assertEqual(expected_content_1, migrations[0].script)
        self.assertEqual(expected_content_2, migrations[1].script)
