import logging
from datetime import datetime
from sqlite3 import Connection
from typing import List

from symigrate.defaults import SYMIGRATE_TIMESTAMP_FORMAT
from symigrate.executed_migration_repository_statements import QUERY_FIND_MIGRATION_BY_SCOPE, QUERY_INSERT_MIGRATION, \
    DDL_CREATE_MIGRATION_TABLE, QUERY_FIND_MIGRATION_TABLE
from symigrate.migration import Migration
from symigrate.migration_execution_result import MigrationExecutionResult

LOGGER = logging.getLogger(__name__)


class ExecutedMigrationRepository:

    def __init__(self, database_connection: Connection):
        self.database_connection = database_connection

    def _create_schema(self):
        LOGGER.info("Initializing migration database")
        self.database_connection.execute(DDL_CREATE_MIGRATION_TABLE)

    def _schema_exists(self) -> bool:
        row = self.database_connection.execute(QUERY_FIND_MIGRATION_TABLE).fetchone()

        return int(row[0]) > 0

    def init(self):
        if not self._schema_exists():
            self._create_schema()

    def push(self, migration: Migration):
        LOGGER.debug("Saving executed migration %s", migration)
        self.database_connection.execute(QUERY_INSERT_MIGRATION, (
            migration.version,
            migration.description,
            migration.execution_result.execution_timestamp.strftime(SYMIGRATE_TIMESTAMP_FORMAT),
            migration.get_status_as_string(),
            migration.checksum,
            migration.execution_result.stdout,
            migration.execution_result.stderr,
            migration.scope,
            migration.script,
            migration.filename
        ))

        self.database_connection.commit()

    def find_by_scope(self, scope: str) -> List[Migration]:
        LOGGER.debug("Looking for executed migrations for scope '%s'", scope)
        cursor = self.database_connection.execute(QUERY_FIND_MIGRATION_BY_SCOPE, (scope,))
        migrations = [self._create_migration_from_row(row) for row in cursor]

        LOGGER.debug("Found %d executed migrations for scope '%s'", len(migrations), scope)

        return migrations

    @staticmethod
    def _create_migration_from_row(row):
        migration_execution_result = MigrationExecutionResult(
            stdout=row[5],
            stderr=row[6],
            execution_timestamp=datetime.strptime(row[2], SYMIGRATE_TIMESTAMP_FORMAT),

        )
        migration = Migration(
            version=row[0],
            description=row[1],
            status=row[3].split(","),
            checksum=row[4],
            scope=row[7],
            script=row[8],
            execution_result=migration_execution_result,
            filename=row[9]
        )
        return migration
