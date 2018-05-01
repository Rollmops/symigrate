import sqlite3
import unittest
from io import StringIO
from unittest.mock import Mock

from symigrate.main.symigrate import InterfaceCreationPhase, MainPhase, CommandlineParsePhase
from symigrate.migration import Migration
from symigrate.migration_execution_result import MigrationExecutionResult
from symigrate.repository.executed_migration_repository_statements import DDL_CREATE_MIGRATION_TABLE


class MigrateCommandAcceptanceTestCase(unittest.TestCase):
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

    def test_no_migrations_at_all(self):
        self.migration_script_repository_mock.find_all.return_value = []
        commandline_parse_phase = CommandlineParsePhase()

        with self.assertLogs() as cm:
            commandline_parse_phase.start(args=["migrate"])

        self.assertIn("INFO:symigrate.command.migrate_command:No pending migrations found", cm.output)

    def test_no_pending_migrations(self):
        self.database_connection.execute(
            "INSERT INTO migration (scope, version, description, status, timestamp, checksum)"
            "VALUES"
            "('DEFAULT', '1.0.0', 'test migration', 'SUCCESS', '2018-04-29T11:40:00', '1234')"
        )
        self.migration_script_repository_mock.find_all.return_value = [
            Migration(version="1.0.0", description="test migration", checksum="1234", script="", filename="")
        ]

        commandline_parse_phase = CommandlineParsePhase()

        with self.assertLogs() as cm:
            commandline_parse_phase.start(args=["migrate"])

        self.assertIn("INFO:symigrate.command.migrate_command:No pending migrations found", cm.output)

    def test_one_pending_migration_success(self):
        self.migration_script_repository_mock.find_all.return_value = [
            Migration(
                version="1.0.0", description="test migration", checksum="1234", script="", filename="V1.0.0_descr.sh")
        ]

        commandline_parse_phase = CommandlineParsePhase()
        self.migration_script_runner_mock.run_migration_script.return_value = MigrationExecutionResult(success=True)

        with self.assertLogs() as cm:
            commandline_parse_phase.start(args=["--migration-path", "/path", "migrate"])

        self.migration_script_runner_mock.run_migration_script.assert_called_once_with("/path/V1.0.0_descr.sh")

        self.assertIn("INFO:symigrate.command.migrate_command:Found 1 pending migrations", cm.output)

        migration_table_row = self.database_connection.execute("SELECT version, status FROM migration").fetchone()
        self.assertIsNotNone(migration_table_row)
        self.assertEqual("1.0.0", migration_table_row[0])
        self.assertEqual("SUCCESS", migration_table_row[1])

    def test_one_pending_migration_failed(self):
        self.migration_script_repository_mock.find_all.return_value = [
            Migration(
                version="1.0.0", description="test migration", checksum="1234", script="", filename="V1.0.0_descr.sh")
        ]

        commandline_parse_phase = CommandlineParsePhase()
        self.migration_script_runner_mock.run_migration_script.return_value = MigrationExecutionResult(success=False)

        with self.assertLogs() as cm:
            with self.assertRaises(SystemExit):
                commandline_parse_phase.start(args=["--migration-path", "/path", "migrate"])

        self.migration_script_runner_mock.run_migration_script.assert_called_once_with("/path/V1.0.0_descr.sh")

        self.assertIn("INFO:symigrate.command.migrate_command:Found 1 pending migrations", cm.output)
        self.assertIn(
            "ERROR:symigrate.main.symigrate:StopOnMigrationError: Stopping migration due to failed "
            "migration script execution", cm.output
        )

        migration_table_row = self.database_connection.execute("SELECT version, status FROM migration").fetchone()
        self.assertIsNotNone(migration_table_row)
        self.assertEqual("1.0.0", migration_table_row[0])
        self.assertEqual("FAILED", migration_table_row[1])

    def test_single_migration(self):
        def call_single_migration(expected_version: str, expected_entries_in_table: int, pending_migrations_found: int):
            with self.assertLogs() as _cm:
                commandline_parse_phase.start(args=["--migration-path", "/path", "migrate", "--single"])

            self.assertIn(
                "INFO:symigrate.command.migrate_command:Found %d pending migrations" % pending_migrations_found,
                _cm.output)
            self.assertIn(
                "INFO:symigrate.command.migrate_command:Only executing the next pending migration", _cm.output)

            migration_table_rows = self.database_connection.execute("SELECT version, status FROM migration").fetchall()
            self.assertEqual(expected_entries_in_table, len(migration_table_rows))
            self.assertEqual(expected_version, migration_table_rows[-1][0])
            self.assertEqual("SUCCESS", migration_table_rows[-1][1])

        self.migration_script_repository_mock.find_all.return_value = [
            Migration(
                version="1.0.0", description="first migration", checksum="1234", script="", filename="V1.0.0_descr.sh"),
            Migration(
                version="1.1.0", description="second migration", checksum="2345", script="",
                filename="V1.1.0_descr.sh"),
        ]
        commandline_parse_phase = CommandlineParsePhase()
        self.migration_script_runner_mock.run_migration_script.return_value = MigrationExecutionResult(success=True)

        # first single migration call
        call_single_migration(expected_version="1.0.0", expected_entries_in_table=1, pending_migrations_found=2)
        # second single migration call
        call_single_migration(expected_version="1.1.0", expected_entries_in_table=2, pending_migrations_found=1)

        with self.assertLogs() as cm:
            commandline_parse_phase.start(args=["--migration-path", "/path", "migrate", "--single"])

        self.assertIn("INFO:symigrate.command.migrate_command:No pending migrations found", cm.output)
