import hashlib
import os
import re
from typing import List

from symigrate.migration import Migration


class MigrationRepository:
    ENCODING = "utf-8"

    def __init__(self, path: str, scope: str = "DEFAULT"):
        self.path = path
        self.scope = scope
        self._regex = re.compile(r"^V(\S+)__(\S+)\.sh")

    def find_all(self) -> List[Migration]:
        migrations = (self._create_migration(regex_match) for regex_match in self._iterate_relevant_migration_files())

        return sorted(migrations, key=lambda migration: migration.version)

    def _iterate_relevant_migration_files(self):
        for filename in os.listdir(self.path):
            regex_match = self._regex.match(filename)
            if regex_match is not None:
                yield regex_match

    def _create_migration(self, regex_match):
        file_path = os.path.join(self.path, regex_match.group(0))
        migration_script_content = self._get_script_content(file_path)
        migration = Migration(
            version=regex_match.group(1),
            description=regex_match.group(2).replace("_", " "),
            checksum=self._calculate_checksum(migration_script_content),
            script=migration_script_content,
            scope=self.scope
        )
        return migration

    @staticmethod
    def _get_script_content(path: str) -> str:
        with open(path, encoding=MigrationRepository.ENCODING) as fp:
            return fp.read()

    @staticmethod
    def _calculate_checksum(content: str) -> str:
        checksum = hashlib.md5()
        checksum.update(content.encode(MigrationRepository.ENCODING))
        return checksum.hexdigest()
