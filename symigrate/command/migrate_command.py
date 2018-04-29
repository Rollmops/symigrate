import os
import sys

from symigrate.executed_migration_repository import ExecutedMigrationRepository
from symigrate.migration_merge_service import MigrationMergeService
from symigrate.migration_repository import MigrationRepository
from symigrate.migration_script_runner import MigrationScriptRunner
from symigrate.migration_status import MigrationStatus


class MigrateCommand:
    def __init__(
            self, migration_repository: MigrationRepository,
            executed_migration_repository: ExecutedMigrationRepository,
            migration_merge_service: MigrationMergeService,
            migration_script_runner: MigrationScriptRunner,
            scope: str,
            migration_path: str,
            out_stream=None
    ):
        self.migration_repository = migration_repository
        self.executed_migration_repository = executed_migration_repository
        self.migration_merge_service = migration_merge_service
        self.migration_script_runner = migration_script_runner
        self.scope = scope
        self.migration_path = migration_path
        self.out_stream = out_stream or sys.stdout

    def run(self):
        executed_migrations = self.executed_migration_repository.find_by_scope(self.scope)
        migrations = self.migration_repository.find_all()

        merged_migrations = self.migration_merge_service.merge(migrations, executed_migrations)

        for merged_migration in merged_migrations:
            if merged_migration.status == [MigrationStatus.PENDING]:
                migration_script_path = os.path.join(self.migration_path, merged_migration.filename)
                self.migration_script_runner.run_migration_script(migration_script_path)
