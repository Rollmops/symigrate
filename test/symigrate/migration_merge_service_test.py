import unittest

from symigrate.migration import Migration
from symigrate.migration_merge_service import MigrationMergeService
from symigrate.migration_status import MigrationStatus


class MigrationMergeServiceTestCase(unittest.TestCase):
    def test_all_pending(self):
        migrations = [
            Migration("1.0.0", None, None, None, None),
            Migration("1.2.0", None, None, None, None),
            Migration("1.3.0", None, None, None, None),
        ]
        executed_migrations = []

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[0].get_status_as_string())
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[1].get_status_as_string())
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[2].get_status_as_string())

    def test_first_migration_was_executed(self):
        migrations = [
            Migration("1.0.0", None, None, None, None),
            Migration("1.2.0", None, None, None, None),
            Migration("1.3.0", None, None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, None, None, None, status=[MigrationStatus.SUCCESS])
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(MigrationStatus.SUCCESS, merged_migrations[0].get_status_as_string())
        self.assertEqual(executed_migrations[0], merged_migrations[0])
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[1].get_status_as_string())
        self.assertEqual(MigrationStatus.PENDING, merged_migrations[2].get_status_as_string())

    def test_all_migrations_were_executed(self):
        migrations = [
            Migration("1.0.0", None, None, None, None),
            Migration("1.2.0", None, None, None, None),
            Migration("1.3.0", None, None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, None, None, None, status=[MigrationStatus.SUCCESS]),
            Migration("1.2.0", None, None, None, None, status=[MigrationStatus.SUCCESS]),
            Migration("1.3.0", None, None, None, None, status=[MigrationStatus.FAILED])
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(executed_migrations[0], merged_migrations[0])
        self.assertEqual(executed_migrations[1], merged_migrations[1])
        self.assertEqual(executed_migrations[2], merged_migrations[2])
        self.assertEqual(MigrationStatus.FAILED, merged_migrations[2].get_status_as_string())

    def test_missing_migration_script(self):
        migrations = [
            Migration("1.0.0", None, None, None, None),
            Migration("1.2.0", None, None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, None, None, None, status=[MigrationStatus.SUCCESS]),
            Migration("1.2.0", None, None, None, None, status=[MigrationStatus.SUCCESS]),
            Migration("1.3.0", None, None, None, None, status=[MigrationStatus.FAILED])
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(3, len(merged_migrations))
        self.assertEqual(executed_migrations[0], merged_migrations[0])
        self.assertEqual(executed_migrations[1], merged_migrations[1])
        self.assertEqual(executed_migrations[2], merged_migrations[2])
        self.assertEqual(
            [MigrationStatus.FAILED, MigrationStatus.MISSING_MIGRATION_SCRIPT], merged_migrations[2].status
        )

    def test_incorrect_checksum(self):
        migrations = [
            Migration("1.0.0", None, "1234", None, None),
            Migration("1.2.0", None, None, None, None),
        ]
        executed_migrations = [
            Migration("1.0.0", None, "4321", None, None, status=[MigrationStatus.SUCCESS]),
            Migration("1.2.0", None, None, None, None, status=[MigrationStatus.SUCCESS]),
        ]

        merged_migrations = MigrationMergeService().merge(migrations, executed_migrations)

        self.assertEqual(2, len(merged_migrations))
        self.assertEqual([MigrationStatus.SUCCESS, MigrationStatus.CHECKSUM_MISMATCH], merged_migrations[0].status)
