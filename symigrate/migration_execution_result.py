from datetime import datetime


class MigrationExecutionResult:
    def __init__(
            self,
            execution_timestamp: datetime = None,
            success: bool = False
    ):
        self.execution_timestamp = execution_timestamp or datetime.now()
        self.success = success
