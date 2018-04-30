import sqlite3
import unittest

from symigrate.defaults import SYMIGRATE_DEFAULT_SCOPE
from symigrate.migration import Migration
from symigrate.migration_execution_result import MigrationExecutionResult
from symigrate.migration_status import MigrationStatus
from symigrate.repository.executed_migration_repository import ExecutedMigrationRepository


class ExecutedMigrationRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database_connection = sqlite3.connect(":memory:").cursor().connection
        self.executed_migration_repository = ExecutedMigrationRepository(
            SYMIGRATE_DEFAULT_SCOPE, self.database_connection
        )

    def test_create_initial_schema(self):
        self.executed_migration_repository.init()

        rows = self.database_connection.execute("SELECT * FROM migration").fetchall()

        self.assertEqual(0, len(rows))

    def test_push(self):
        migration = Migration(
            "1.2.3", "some description",
            status=[MigrationStatus.SUCCESS],
            checksum="1234",
            script="echo 'huhu'",
            execution_result=MigrationExecutionResult(),
            filename="V1.2.3__some_description.sh"
        )

        self.executed_migration_repository.init()
        self.executed_migration_repository.push(migration)

        rows = self.database_connection.execute(
            "SELECT version, description, status, "
            "checksum, scope, script FROM migration").fetchall()

        self.assertEqual(1, len(rows))
        row = rows[0]

        self.assertEqual("1.2.3", row[0])
        self.assertEqual("some description", row[1])
        self.assertEqual("SUCCESS", row[2])
        self.assertEqual("1234", row[3])
        self.assertEqual("DEFAULT", row[4])
        self.assertEqual("echo 'huhu'", row[5])
