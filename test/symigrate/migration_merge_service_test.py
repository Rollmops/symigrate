import unittest

from symigrate.migration import Migration
from symigrate.migration_merge_service import MigrationMergeService
from symigrate.migration_status import MigrationStatus


class MigrationMergeServiceTestCase(unittest.TestCase):
    def test_all_pending(self):
        migrations = [
            Migration("1.0.0", None, None, None),
            Migration("1.2.0", None, None, None),
            Migration("1.3.0", None, None, None),
        ]
        executed_migrations = []

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[0].status)
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[1].status)
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[2].status)

    def test_first_migration_was_executed(self):
        migrations = [
            Migration("1.0.0", None, None, None),
            Migration("1.2.0", None, None, None),
            Migration("1.3.0", None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, None, None, status=MigrationStatus.SUCCESSFUL)
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(MigrationStatus.SUCCESSFUL, merged_migrations[0].status)
        self.assertEqual(executed_migrations[0], merged_migrations[0])
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[1].status)
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[2].status)

    def test_all_migrations_were_executed(self):
        migrations = [
            Migration("1.0.0", None, None, None),
            Migration("1.2.0", None, None, None),
            Migration("1.3.0", None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, None, None, status=MigrationStatus.SUCCESSFUL),
            Migration("1.2.0", None, None, None, status=MigrationStatus.SUCCESSFUL),
            Migration("1.3.0", None, None, None, status=MigrationStatus.FAILED)
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(executed_migrations[0], merged_migrations[0])
        self.assertEqual(executed_migrations[1], merged_migrations[1])
        self.assertEqual(executed_migrations[2], merged_migrations[2])
        self.assertEqual(MigrationStatus.FAILED, merged_migrations[2].status)

    def test_more_executed_migrations_than_files(self):
        migrations = [
            Migration("1.0.0", None, None, None),
            Migration("1.2.0", None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, None, None, status=MigrationStatus.SUCCESSFUL),
            Migration("1.2.0", None, None, None, status=MigrationStatus.SUCCESSFUL),
            Migration("1.3.0", None, None, None, status=MigrationStatus.FAILED)
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(executed_migrations[0], merged_migrations[0])
        self.assertEqual(executed_migrations[1], merged_migrations[1])
        self.assertEqual(executed_migrations[2], merged_migrations[2])
        self.assertEqual(MigrationStatus.FAILED, merged_migrations[2].status)
