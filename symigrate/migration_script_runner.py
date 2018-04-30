import logging
import subprocess
from datetime import datetime

from symigrate.defaults import SYMIGRATE_SCRIPT_EXECUTION_TIMEOUT
from symigrate.migration_execution_result import MigrationExecutionResult

LOGGER = logging.getLogger(__name__)


class MigrationScriptRunner:
    def __init__(self, timeout: int = SYMIGRATE_SCRIPT_EXECUTION_TIMEOUT):
        # TODO timeout needed?
        self.timeout = timeout

    @staticmethod
    def run_migration_script(migration_file_path: str) -> MigrationExecutionResult:
        LOGGER.info("Running migration script '%s'", migration_file_path)
        migration_execution_result = MigrationExecutionResult(
            stdout="",
            stderr="",
            execution_timestamp=datetime.now()
        )

        try:
            subprocess.call(migration_file_path)
        except Exception as exception:
            LOGGER.error(repr(exception))
            migration_execution_result.success = False
        else:
            migration_execution_result.success = True

        return migration_execution_result
