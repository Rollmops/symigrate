import logging
import os
import sys
from typing import List

from symigrate import SymigrateException
from symigrate.migration import Migration
from symigrate.migration_merge_service import MigrationMergeService
from symigrate.migration_script_checker import MigrationScriptChecker
from symigrate.migration_script_runner import MigrationScriptRunner
from symigrate.migration_status import MigrationStatus
from symigrate.repository.executed_migration_repository import ExecutedMigrationRepository
from symigrate.repository.migration_script_repository import MigrationScriptRepository

LOGGER = logging.getLogger(__name__)


class MigrateCommand:
    def __init__(
            self, migration_script_repository: MigrationScriptRepository,
            executed_migration_repository: ExecutedMigrationRepository,
            migration_merge_service: MigrationMergeService,
            migration_script_runner: MigrationScriptRunner,
            migration_script_checker: MigrationScriptChecker,
            migration_path: str,
            single: bool,
            out_stream=None,
    ):
        self.migration_script_repository = migration_script_repository
        self.executed_migration_repository = executed_migration_repository
        self.migration_merge_service = migration_merge_service
        self.migration_script_runner = migration_script_runner
        self.migration_script_checker = migration_script_checker
        self.migration_path = migration_path
        self.single = single
        self.out_stream = out_stream or sys.stdout

    def run(self):
        executed_migrations = self.executed_migration_repository.find_all()
        migrations = self.migration_script_repository.find_all()

        merged_migrations = self.migration_merge_service.merge(migrations, executed_migrations)
        pending_migrations = self._get_pending_migrations(merged_migrations)

        if not pending_migrations:
            LOGGER.info("No pending migrations found")
        else:
            self._migrate(pending_migrations)

    def _migrate(self, pending_migrations):
        LOGGER.info("Found %d pending migrations", len(pending_migrations))
        if self.single:
            LOGGER.info("Only executing the next pending migration")
            pending_migrations = pending_migrations[:1]
        self._check_pending_migrations(pending_migrations)
        for pending_migration in pending_migrations:
            migration_script_path = os.path.join(self.migration_path, pending_migration.filename)
            self._run_migration(pending_migration, migration_script_path)

    def _check_pending_migrations(self, pending_migrations: List[Migration]):
        for pending_migration in pending_migrations:
            self.migration_script_checker.check(pending_migration.full_file_path)

    @staticmethod
    def _get_pending_migrations(migrations: List[Migration]) -> List[Migration]:
        pending_migrations = [migration for migration in migrations if migration.status == [MigrationStatus.PENDING]]
        return pending_migrations

    def _run_migration(self, merged_migration, migration_script_path):
        migration_execution_result = self.migration_script_runner.run_migration_script(migration_script_path)
        merged_migration.execution_result = migration_execution_result
        merged_migration.status = \
            [MigrationStatus.SUCCESS] if migration_execution_result.success else [MigrationStatus.FAILED]
        self.executed_migration_repository.push(merged_migration)
        if not migration_execution_result.success:
            raise MigrateCommand.StopOnMigrationError("Stopping migration due to failed migration script execution")

    class StopOnMigrationError(SymigrateException):
        pass
