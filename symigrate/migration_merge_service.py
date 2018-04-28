from typing import List

from symigrate.migration import Migration


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
        return merged_migrations
