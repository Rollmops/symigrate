import hashlib
import logging
import os
from typing import List, Union

from symigrate.migration import Migration
from symigrate.migration_file_matcher import MigrationFileMatcher

LOGGER = logging.getLogger(__name__)


class MigrationRepository:
    def __init__(
            self,
            path: str,
            scope: str,
            encoding: str,
            migration_file_matcher: MigrationFileMatcher
    ):
        self.path = path
        self.scope = scope
        self.encoding = encoding
        self.migration_file_matcher = migration_file_matcher

    def find_all(self) -> List[Migration]:
        LOGGER.debug("Looking for migration scripts in: %s", self.path)
        migrations = (self._create_migration(match_result) for match_result in self._iterate_relevant_migration_files())

        sorted_migrations = sorted(migrations, key=lambda migration: migration.version)
        LOGGER.debug("Found %d migration scripts", len(sorted_migrations))
        return sorted_migrations

    def find_by_version(self, version: str) -> Union[Migration, None]:
        return next((migration for migration in self.find_all() if migration.version == version), None)

    def _iterate_relevant_migration_files(self):
        for filename in sorted(os.listdir(self.path)):
            match_result = self.migration_file_matcher.match(filename)
            if match_result is not None:
                LOGGER.debug("Found migration script: %s", filename)
                yield match_result
            else:
                LOGGER.debug("Ignoring file '%s'", filename)

    def _create_migration(self, match_result: MigrationFileMatcher.MatchResult):
        full_file_path = os.path.join(self.path, match_result.filename)
        migration_script_content = self._get_script_content(full_file_path)
        migration = Migration(
            version=match_result.version,
            description=match_result.description,
            checksum=self._calculate_checksum(migration_script_content),
            script=migration_script_content,
            scope=self.scope,
            filename=match_result.filename,
            full_file_path=full_file_path
        )
        return migration

    def _get_script_content(self, path: str) -> str:
        with open(path, encoding=self.encoding) as fp:
            return fp.read()

    def _calculate_checksum(self, content: str) -> str:
        checksum = hashlib.md5()
        checksum.update(content.encode(self.encoding))
        return checksum.hexdigest()
