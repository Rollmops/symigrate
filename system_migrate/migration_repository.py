from datetime import datetime
from sqlite3 import Connection

from system_migrate.migration import Migration


class MigrationRepository:
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
        cursor = self.database_connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='migration'"
        )

        return cursor.rowcount > 0

    def init(self):
        if not self._schema_exists():
            self._create_schema()

    def push(self, migration: Migration):
        self.database_connection.execute(
            "INSERT INTO migration "
            "(id, version, description, timestamp, status, checksum, stdout, stderr, scope, script) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                migration.id,
                migration.version,
                migration.description,
                migration.timestamp.strftime(MigrationRepository.TIMESTAMP_FORMAT),
                migration.status,
                migration.checksum,
                migration.stdout,
                migration.stderr,
                migration.scope,
                migration.script

            )
        )

        self.database_connection.commit()

    def find_by_id(self, id: str) -> Migration:
        row = self.database_connection.execute(
            "SELECT version, description, timestamp, status, checksum, stdout, stderr, scope, script FROM migration"
        ).fetchone()

        if not row:
            raise MigrationRepository.MigrationNotFoundException("Unable to find migration for id '{id}'".format(id=id))

        migration = Migration(
            id=id,
            version=row[0],
            description=row[1],
            timestamp=datetime.strptime(row[2], MigrationRepository.TIMESTAMP_FORMAT),
            status=row[3],
            checksum=row[4],
            stdout=row[5],
            stderr=row[6],
            scope=row[7],
            script=row[8]
        )

        return migration

    class MigrationNotFoundException(Exception):
        pass
