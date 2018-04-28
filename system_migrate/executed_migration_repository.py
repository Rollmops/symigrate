from datetime import datetime
from sqlite3 import Connection
from typing import List

from system_migrate.executed_migration import ExecutedMigration


class ExecutedMigrationRepository:
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, database_connection: Connection):
        self.database_connection = database_connection

    def _create_schema(self):
        self.database_connection.execute("""
        CREATE TABLE migration 
        (id TEXT, version TEXT, description TEXT, timestamp TEXT, status TEXT, 
        checksum TEXT, stdout TEXT, stderr TEXT, scope TEXT, script TEXT)
        """)

    def _schema_exists(self) -> bool:
        row = self.database_connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='migration'"
        ).fetchone()

        return int(row[0]) > 0

    def init(self):
        if not self._schema_exists():
            self._create_schema()

    def push(self, migration: ExecutedMigration):
        self.database_connection.execute(
            "INSERT INTO migration "
            "(id, version, description, timestamp, status, checksum, stdout, stderr, scope, script) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                migration.id,
                migration.version,
                migration.description,
                migration.timestamp.strftime(ExecutedMigrationRepository.TIMESTAMP_FORMAT),
                migration.status,
                migration.checksum,
                migration.stdout,
                migration.stderr,
                migration.scope,
                migration.script

            )
        )

        self.database_connection.commit()

    def find_all(self) -> List[ExecutedMigration]:
        cursor = self.database_connection.execute(
            "SELECT version, description, timestamp, status, checksum, stdout, stderr, scope, script, id "
            "FROM migration "
            "ORDER BY version"
        )

        migrations = [self._create_executed_migration_from_row(row) for row in cursor]

        return migrations

    def find_by_scope(self, scope: str) -> List[ExecutedMigration]:
        cursor = self.database_connection.execute(
            "SELECT version, description, timestamp, status, checksum, stdout, stderr, scope, script, id "
            "FROM migration "
            "WHERE scope = ? "
            "ORDER BY version", (scope,)
        )

        migrations = [self._create_executed_migration_from_row(row) for row in cursor]

        return migrations

    @staticmethod
    def _create_executed_migration_from_row(row):
        migration = ExecutedMigration(
            id=row[9],
            version=row[0],
            description=row[1],
            timestamp=datetime.strptime(row[2], ExecutedMigrationRepository.TIMESTAMP_FORMAT),
            status=row[3],
            checksum=row[4],
            stdout=row[5],
            stderr=row[6],
            scope=row[7],
            script=row[8]
        )
        return migration
