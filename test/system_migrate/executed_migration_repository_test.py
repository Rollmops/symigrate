import sqlite3
import unittest
from datetime import datetime

from system_migrate.executed_migration import ExecutedMigration
from system_migrate.executed_migration_repository import ExecutedMigrationRepository


class ExecutedMigrationRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database_connection = sqlite3.connect(":memory:").cursor().connection
        self.executed_migration_repository = ExecutedMigrationRepository(self.database_connection)

    def test_create_initial_schema(self):
        self.executed_migration_repository.init()

        rows = self.database_connection.execute("SELECT * FROM migration").fetchall()

        self.assertEqual(0, len(rows))

    def test_push(self):
        migration = ExecutedMigration(
            "1.2.3", "some description",
            status="SUCCESS", stdout="stdout output", stderr="error output", checksum="1234", script="echo 'huhu'")

        self.executed_migration_repository.init()
        self.executed_migration_repository.push(migration)

        rows = self.database_connection.execute(
            "SELECT version, description, status, stdout, stderr, "
            "checksum, id, scope, script FROM migration").fetchall()

        self.assertEqual(1, len(rows))
        row = rows[0]

        self.assertEqual("1.2.3", row[0])
        self.assertEqual("some description", row[1])
        self.assertEqual("SUCCESS", row[2])
        self.assertEqual("stdout output", row[3])
        self.assertEqual("error output", row[4])
        self.assertEqual("1234", row[5])
        self.assertEqual(32, len(row[6]))
        self.assertEqual("DEFAULT", row[7])
        self.assertEqual("echo 'huhu'", row[8])

    def test_find_all(self):
        migration = ExecutedMigration(
            version="1.2.3", description="some description", id="1", timestamp=datetime(2018, 4, 28, 15, 48),
            status="SUCCESS", stdout="stdout output", stderr="error output", checksum="1234", script="echo 'huhu'"
        )

        self.executed_migration_repository.init()
        self.executed_migration_repository.push(migration)

        stored_migrations = self.executed_migration_repository.find_all()
        stored_migration = stored_migrations[0]

        self.assertEqual("1.2.3", stored_migration.version)
        self.assertEqual("some description", stored_migration.description)
        self.assertEqual("1", stored_migration.id)
        self.assertEqual(datetime(2018, 4, 28, 15, 48), stored_migration.timestamp)
        self.assertEqual("SUCCESS", stored_migration.status)
        self.assertEqual("stdout output", stored_migration.stdout)
        self.assertEqual("error output", stored_migration.stderr)
        self.assertEqual("1234", stored_migration.checksum)
        self.assertEqual("echo 'huhu'", stored_migration.script)
