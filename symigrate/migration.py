from symigrate.migration_execution_result import MigrationExecutionResult
from symigrate.migration_status import MigrationStatus


class Migration:
    def __init__(
            self, version: str,
            description: str,
            checksum: str,
            script: str,
            status: str = MigrationStatus.PENDING,
            scope: str = "DEFAULT",
            execution_result: MigrationExecutionResult = None
    ):
        self.version = version
        self.description = description
        self.status = status
        self.checksum = checksum
        self.script = script
        self.scope = scope
        self.execution_result = execution_result
