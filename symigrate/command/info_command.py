import logging
import sys

from tabulate import tabulate

from symigrate.defaults import SYMIGRATE_DEFAULT_SCOPE
from symigrate.executed_migration_repository import ExecutedMigrationRepository
from symigrate.migration import Migration
from symigrate.migration_merge_service import MigrationMergeService
from symigrate.migration_repository import MigrationRepository

LOGGER = logging.getLogger(__name__)


class InfoCommand:
    def __init__(
            self,
            executed_migration_repository: ExecutedMigrationRepository,
            migration_repository: MigrationRepository,
            migration_merge_service: MigrationMergeService,
            scope: str = SYMIGRATE_DEFAULT_SCOPE,
            out_stream=None
    ):
        self.executed_migration_repository = executed_migration_repository
        self.migration_repository = migration_repository
        self.migration_merge_service = migration_merge_service
        self.scope = scope
        self.out_stream = out_stream or sys.stdout

    def run(self):
        executed_migrations = self.executed_migration_repository.find_all()
        migrations = self.migration_repository.find_all()

        merged_migrations = self.migration_merge_service.merge(migrations, executed_migrations)

        table = [self._get_table_row_from_migration(migration) for migration in merged_migrations]
        header = ["Version", "Description", "Migration Date", "Status"]

        self.out_stream.write("Scope: {scope}\n".format(scope=self.scope))
        self.out_stream.write(tabulate(table, header, "grid", disable_numparse=True))
        self.out_stream.write("\n")

    @staticmethod
    def _get_table_row_from_migration(migration: Migration) -> list:
        return [
            migration.version,
            migration.description,
            migration.execution_result.execution_timestamp if migration.execution_result is not None else "",
            migration.get_status_as_string()
        ]
