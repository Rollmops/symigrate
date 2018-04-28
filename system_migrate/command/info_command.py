import logging
import sys

from tabulate import tabulate

from system_migrate.executed_migration_repository import ExecutedMigrationRepository
from system_migrate.migration import Migration
from system_migrate.migration_merge_service import MigrationMergeService
from system_migrate.migration_repository import MigrationRepository

LOGGER = logging.getLogger(__name__)


class InfoCommand:
    def __init__(
            self,
            executed_migration_repository: ExecutedMigrationRepository,
            migration_repository: MigrationRepository,
            migration_merge_service: MigrationMergeService,
            scope: str = "DEFAULT",
            out_stream=None
    ):
        self.executed_migration_repository = executed_migration_repository
        self.migration_repository = migration_repository
        self.migration_merge_service = migration_merge_service
        self.scope = scope
        self.out_stream = out_stream or sys.stdout

    def run(self):
        executed_migrations = self.executed_migration_repository.find_by_scope(self.scope)
        migrations = self.migration_repository.find_all()

        merged_migrations = self.migration_merge_service.merge(migrations, executed_migrations)

        table = [self._get_table_row_from_migration(migration) for migration in merged_migrations]
        header = ["Scope", "Version", "Description", "Status"]

        self.out_stream.write(tabulate(table, header, "grid"))
        self.out_stream.write("\n")

    @staticmethod
    def _get_table_row_from_migration(migration: Migration) -> list:
        return [migration.scope, migration.version, migration.description, migration.status]
