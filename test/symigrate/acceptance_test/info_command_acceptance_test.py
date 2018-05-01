import os
import sqlite3
import unittest
from io import StringIO
from unittest.mock import Mock

from symigrate.main.symigrate import CommandlineParsePhase, InterfaceCreationPhase, MainPhase
from symigrate.migration import Migration
from symigrate.repository.executed_migration_repository_statements import DDL_CREATE_MIGRATION_TABLE
from test.symigrate.helper import dedent_and_remove_white_lines


class InfoCommandAcceptanceTestCase(unittest.TestCase):

    def setUp(self):
        self.migrations_path = os.path.join(os.path.dirname(__file__), "..", "data", "migrations")
        self.assertTrue(os.path.isdir(self.migrations_path))

        self.database_connection = sqlite3.connect(":memory:")
        self.database_connection.execute(DDL_CREATE_MIGRATION_TABLE)
        self.out_stream = StringIO()
        self.migration_script_repository_mock = Mock()
        self.migration_script_repository_mock.find_all = Mock()
        self.migration_script_repository_mock.find_all.return_value = [
            Migration(version="1.0.0", description="test migration", checksum="1234", script="", filename=""),
            Migration(version="1.1.0", description="another migration", checksum="1234", script="", filename=""),
        ]
        InterfaceCreationPhase.database_connection_hook = self.database_connection
        MainPhase.out_stream_hook = self.out_stream
        MainPhase.migration_script_checker_hook = Mock()
        MainPhase.migration_script_repository_hook = self.migration_script_repository_mock

    def test_info_no_scope(self):
        commandline_parse_phase = CommandlineParsePhase()

        commandline_parse_phase.start(["--migration-path", self.migrations_path, "info"])

        expected_output = dedent_and_remove_white_lines("""
            Scope: DEFAULT
            +-----------+-------------------+------------------+----------+
            | Version   | Description       | Migration Date   | Status   |
            +===========+===================+==================+==========+
            | 1.0.0     | test migration    |                  | PENDING  |
            +-----------+-------------------+------------------+----------+
            | 1.1.0     | another migration |                  | PENDING  |
            +-----------+-------------------+------------------+----------+
        """)

        self.assertEqual(expected_output, self.out_stream.getvalue())

    def test_info_custom_scope(self):
        commandline_parse_phase = CommandlineParsePhase()

        commandline_parse_phase.start(["--migration-path", self.migrations_path, "--scope", "my_scope", "info"])

        expected_output = dedent_and_remove_white_lines("""
            Scope: my_scope
            +-----------+-------------------+------------------+----------+
            | Version   | Description       | Migration Date   | Status   |
            +===========+===================+==================+==========+
            | 1.0.0     | test migration    |                  | PENDING  |
            +-----------+-------------------+------------------+----------+
            | 1.1.0     | another migration |                  | PENDING  |
            +-----------+-------------------+------------------+----------+
        """)

        self.assertEqual(expected_output, self.out_stream.getvalue())

    def test_info_with_already_executed_migrations(self):
        self.database_connection.execute(
            "INSERT INTO migration (scope, version, description, status, timestamp, checksum)"
            "VALUES"
            "('DEFAULT', '1.0.0', 'test migration', 'SUCCESS', '2018-04-29T11:40:00', '1234')"
        )
        self.database_connection.commit()

        commandline_parse_phase = CommandlineParsePhase()

        commandline_parse_phase.start(["--migration-path", self.migrations_path, "info"])

        expected_output = dedent_and_remove_white_lines("""
            Scope: DEFAULT
            +-----------+-------------------+---------------------+----------+
            | Version   | Description       | Migration Date      | Status   |
            +===========+===================+=====================+==========+
            | 1.0.0     | test migration    | 2018-04-29 11:40:00 | SUCCESS  |
            +-----------+-------------------+---------------------+----------+
            | 1.1.0     | another migration |                     | PENDING  |
            +-----------+-------------------+---------------------+----------+
        """)

        self.assertEqual(expected_output, self.out_stream.getvalue())

    def test_info_with_already_executed_migrations_checksum_mismatch(self):
        self.database_connection.execute(
            "INSERT INTO migration (scope, version, description, status, timestamp, checksum)"
            "VALUES"
            "('DEFAULT', '1.0.0', 'test migration', 'SUCCESS', '2018-04-29T11:40:00', '4321')"
        )
        self.database_connection.commit()

        commandline_parse_phase = CommandlineParsePhase()

        commandline_parse_phase.start(["--migration-path", self.migrations_path, "info"])

        expected_output = dedent_and_remove_white_lines(
            """
            Scope: DEFAULT
            +-----------+-------------------+---------------------+-------------------+
            | Version   | Description       | Migration Date      | Status            |
            +===========+===================+=====================+===================+
            | 1.0.0     | test migration    | 2018-04-29 11:40:00 | SUCCESS, MODIFIED |
            +-----------+-------------------+---------------------+-------------------+
            | 1.1.0     | another migration |                     | PENDING           |
            +-----------+-------------------+---------------------+-------------------+
            """
        )

        self.assertEqual(expected_output, self.out_stream.getvalue())
