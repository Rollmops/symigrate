import hashlib
import os
from typing import List

from symigrate.migration import Migration
from symigrate.migration_file_matcher import MigrationFileMatcher


class MigrationRepository:
    def __init__(self, path: str, scope: str, encoding: str, migration_file_matcher: MigrationFileMatcher):
        self.path = path
        self.scope = scope
        self.encoding = encoding
        self.migration_file_matcher = migration_file_matcher

    def find_all(self) -> List[Migration]:
        migrations = (self._create_migration(match_result) for match_result in self._iterate_relevant_migration_files())

        sorted_migrations = sorted(migrations, key=lambda migration: migration.version)
        return sorted_migrations

    def _iterate_relevant_migration_files(self):
        for filename in os.listdir(self.path):
            match_result = self.migration_file_matcher.match(filename)
            if match_result is not None:
                yield match_result

    def _create_migration(self, match_result: MigrationFileMatcher.MatchResult):
        file_path = os.path.join(self.path, match_result.filename)
        migration_script_content = self._get_script_content(file_path)
        migration = Migration(
            version=match_result.version,
            description=match_result.description,
            checksum=self._calculate_checksum(migration_script_content),
            script=migration_script_content,
            scope=self.scope,
            filename=match_result.filename
        )
        return migration

    def _get_script_content(self, path: str) -> str:
        with open(path, encoding=self.encoding) as fp:
            return fp.read()

    def _calculate_checksum(self, content: str) -> str:
        checksum = hashlib.md5()
        checksum.update(content.encode(self.encoding))
        return checksum.hexdigest()
