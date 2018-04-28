from datetime import datetime

from system_migrate.migration import Migration


class ExecutedMigration(Migration):
    def __init__(
            self, version: str,
            description: str,
            status: str,
            stdout: str,
            stderr: str,
            checksum: str,
            script: str,
            timestamp: datetime = None,
            scope: str = "DEFAULT",
            id: str = None
    ):
        super().__init__(version, description, status, checksum, script, scope, id)

        self.stdout = stdout
        self.stderr = stderr
        self.timestamp = timestamp or datetime.now()
