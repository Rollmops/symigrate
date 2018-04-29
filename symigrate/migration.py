from typing import List

from symigrate.defaults import SYMIGRATE_DEFAULT_SCOPE
from symigrate.migration_execution_result import MigrationExecutionResult
from symigrate.migration_status import MigrationStatus


class Migration:
    def __init__(
            self, version: str,
            description: str,
            checksum: str,
            script: str,
            filename: str,
            status: List[str] = None,
            scope: str = SYMIGRATE_DEFAULT_SCOPE,
            execution_result: MigrationExecutionResult = None
    ):
        self.version = version
        self.description = description
        self.status = status or [MigrationStatus.PENDING]
        self.checksum = checksum
        self.script = script
        self.filename = filename
        self.scope = scope
        self.execution_result = execution_result

    def get_status_as_string(self):
        return ", ".join(self.status)
