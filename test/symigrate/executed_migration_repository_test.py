import sqlite3
import unittest
from datetime import datetime

from symigrate.executed_migration_repository import ExecutedMigrationRepository
from symigrate.migration import Migration
from symigrate.migration_execution_result import MigrationExecutionResult
from symigrate.migration_status import MigrationStatus


class ExecutedMigrationRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database_connection = sqlite3.connect(":memory:").cursor().connection
        self.executed_migration_repository = ExecutedMigrationRepository(self.database_connection)

    def test_create_initial_schema(self):
        self.executed_migration_repository.init()

        rows = self.database_connection.execute("SELECT * FROM migration").fetchall()

        self.assertEqual(0, len(rows))

    def test_push(self):
        migration = Migration(
            "1.2.3", "some description",
            status=[MigrationStatus.SUCCESS], checksum="1234", script="echo 'huhu'",
            execution_result=MigrationExecutionResult(stdout="stdout output", stderr="error output")
        )

        self.executed_migration_repository.init()
        self.executed_migration_repository.push(migration)

        rows = self.database_connection.execute(
            "SELECT version, description, status, stdout, stderr, "
            "checksum, scope, script FROM migration").fetchall()

        self.assertEqual(1, len(rows))
        row = rows[0]

        self.assertEqual("1.2.3", row[0])
        self.assertEqual("some description", row[1])
        self.assertEqual("SUCCESS", row[2])
        self.assertEqual("stdout output", row[3])
        self.assertEqual("error output", row[4])
        self.assertEqual("1234", row[5])
        self.assertEqual("DEFAULT", row[6])
        self.assertEqual("echo 'huhu'", row[7])

    def test_find_all(self):
        migration = Migration(
            version="1.2.3",
            description="some description",
            execution_result=MigrationExecutionResult(
                execution_timestamp=datetime(2018, 4, 28, 15, 48),
                stdout="stdout output",
                stderr="error output"
            ),
            status=[MigrationStatus.SUCCESS], checksum="1234", script="echo 'huhu'"
        )

        self.executed_migration_repository.init()
        self.executed_migration_repository.push(migration)

        stored_migrations = self.executed_migration_repository.find_all()
        stored_migration = stored_migrations[0]

        self.assertEqual("1.2.3", stored_migration.version)
        self.assertEqual("some description", stored_migration.description)
        self.assertEqual(datetime(2018, 4, 28, 15, 48), stored_migration.execution_result.execution_timestamp)
        self.assertEqual("SUCCESS", stored_migration.get_status_as_string())
        self.assertEqual("stdout output", stored_migration.execution_result.stdout)
        self.assertEqual("error output", stored_migration.execution_result.stderr)
        self.assertEqual("1234", stored_migration.checksum)
        self.assertEqual("echo 'huhu'", stored_migration.script)
