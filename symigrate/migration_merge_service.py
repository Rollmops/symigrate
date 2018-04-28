from typing import List

from symigrate.migration import Migration
from symigrate.migration_status import MigrationStatus


class MigrationMergeService:

    @staticmethod
    def merge(migrations: List[Migration], executed_migrations: List[Migration]) -> List[Migration]:
        merged_migrations = executed_migrations

        if executed_migrations:
            last_executed_version = executed_migrations[-1].version
            residual_migrations = [migration for migration in migrations if migration.version > last_executed_version]
        else:
            residual_migrations = migrations

        merged_migrations.extend(residual_migrations)
        MigrationMergeService._check_missing_migration_script(merged_migrations, migrations)
        return merged_migrations

    @staticmethod
    def _check_missing_migration_script(
            merged_migrations: List[Migration], migrations: List[Migration]):
        for merged_migration in merged_migrations:
            if MigrationMergeService._find_by_version(merged_migration.version, migrations) is None:
                merged_migration.status.append(MigrationStatus.MISSING_MIGRATION_SCRIPT)

    @staticmethod
    def _find_by_version(version: str, migrations: List[Migration]):
        return next((migration for migration in migrations if migration.version == version), None)
