import logging
from difflib import ndiff

from symigrate.executed_migration_repository import ExecutedMigrationRepository
from symigrate.migration_repository import MigrationRepository

LOGGER = logging.getLogger(__name__)


class DiffCommand:
    def __init__(
            self,
            version: str,
            migration_repository: MigrationRepository,
            executed_migration_repository: ExecutedMigrationRepository
    ):
        self.version = version
        self.migration_repository = migration_repository
        self.executed_migration_repository = executed_migration_repository

    def run(self):
        executed_migration = self.executed_migration_repository.find_by_version(self.version)
        if not executed_migration:
            LOGGER.warning("Unable to find executed migration for version '%s'", self.version)
            return

        migration = self.migration_repository.find_by_version(self.version)
        if not migration:
            LOGGER.warning("Unable to find migration script for version '%s'", self.version)
            return

        if migration.checksum == executed_migration.checksum:
            LOGGER.info("No difference found")
        else:
            self._print_diff(executed_migration, migration)

    @staticmethod
    def _print_diff(executed_migration, migration):
        diff = ndiff(
            executed_migration.script.splitlines(keepends=True),
            migration.script.splitlines(keepends=True),
        )
        print("".join(diff), end="")
