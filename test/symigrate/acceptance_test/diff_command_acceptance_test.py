import sqlite3
import unittest
from io import StringIO
from unittest.mock import Mock

from symigrate.main.symigrate import MainPhase, InterfaceCreationPhase, CommandlineParsePhase
from symigrate.migration import Migration
from symigrate.repository.executed_migration_repository_statements import DDL_CREATE_MIGRATION_TABLE
from test.symigrate.helper import capture_output


class DiffCommandAcceptanceTestCase(unittest.TestCase):
    def setUp(self):
        self.database_connection = sqlite3.connect(":memory:")
        self.database_connection.execute(DDL_CREATE_MIGRATION_TABLE)
        self.out_stream = StringIO()
        self.migration_script_repository_mock = Mock()
        self.migration_script_repository_mock.find_all = Mock()

        self.migration_script_runner_mock = Mock()
        self.migration_script_runner_mock.run_migration_script = Mock()

        InterfaceCreationPhase.database_connection_hook = self.database_connection
        MainPhase.out_stream_hook = self.out_stream
        MainPhase.migration_script_checker_hook = Mock()
        MainPhase.migration_script_repository_hook = self.migration_script_repository_mock
        MainPhase.migration_script_runner_hook = self.migration_script_runner_mock

    def test_diff_output(self):
        self.database_connection.execute(
            "INSERT INTO migration (scope, version, description, status, timestamp, checksum, script)"
            "VALUES"
            "('DEFAULT', '1.0.0', 'test migration', 'SUCCESS', '2018-04-29T11:40:00', '1234', 'The script')"
        )
        self.migration_script_repository_mock.find_by_version.return_value = \
            Migration(version="1.0.0", description="test migration", checksum="2345", script="", filename="")

        commandline_parse_phase = CommandlineParsePhase()

        with capture_output() as output:
            commandline_parse_phase.start(args=["diff", "--version", "1.0.0"])

        self.assertEqual("- The script", output[0].getvalue())
