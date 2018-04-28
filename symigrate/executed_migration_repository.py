from datetime import datetime
from sqlite3 import Connection
from typing import List

from symigrate.migration import Migration
from symigrate.migration_execution_result import MigrationExecutionResult


class ExecutedMigrationRepository:
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __init__(self, database_connection: Connection):
        self.database_connection = database_connection

    def _create_schema(self):
        self.database_connection.execute("""
        CREATE TABLE migration 
        (version TEXT, description TEXT, timestamp TEXT, status TEXT, 
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

    def push(self, migration: Migration):
        self.database_connection.execute(
            "INSERT INTO migration "
            "(version, description, timestamp, status, checksum, stdout, stderr, scope, script) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                migration.version,
                migration.description,
                migration.execution_result.execution_timestamp.strftime(ExecutedMigrationRepository.TIMESTAMP_FORMAT),
                migration.status,
                migration.checksum,
                migration.execution_result.stdout,
                migration.execution_result.stderr,
                migration.scope,
                migration.script

            )
        )

        self.database_connection.commit()

    def find_all(self) -> List[Migration]:
        cursor = self.database_connection.execute(
            "SELECT version, description, timestamp, status, checksum, stdout, stderr, scope, script "
            "FROM migration "
            "ORDER BY version"
        )

        migrations = [self._create_migration_from_row(row) for row in cursor]

        return migrations

    def find_by_scope(self, scope: str) -> List[Migration]:
        cursor = self.database_connection.execute(
            "SELECT version, description, timestamp, status, checksum, stdout, stderr, scope, script "
            "FROM migration "
            "WHERE scope = ? "
            "ORDER BY version", (scope,)
        )

        migrations = [self._create_migration_from_row(row) for row in cursor]

        return migrations

    @staticmethod
    def _create_migration_from_row(row):
        migration_execution_result = MigrationExecutionResult(
            stdout=row[5],
            stderr=row[6],
            execution_timestamp=datetime.strptime(row[2], ExecutedMigrationRepository.TIMESTAMP_FORMAT),

        )
        migration = Migration(
            version=row[0],
            description=row[1],
            status=row[3],
            checksum=row[4],
            scope=row[7],
            script=row[8],
            execution_result=migration_execution_result
        )
        return migration
