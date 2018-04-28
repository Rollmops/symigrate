from datetime import datetime


class MigrationExecutionResult:
    def __init__(
            self,
            stdout: str,
            stderr: str,
            execution_timestamp: datetime = None
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.execution_timestamp = execution_timestamp or datetime.now()
