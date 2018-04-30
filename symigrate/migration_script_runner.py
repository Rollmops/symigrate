import logging
import subprocess
from datetime import datetime

from symigrate import SymigrateException
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
            return_code = subprocess.call(migration_file_path)
        except Exception as exception:
            LOGGER.error(repr(exception))
            migration_execution_result.success = False
        else:
            LOGGER.debug("Migration script return code: %d", return_code)
            migration_execution_result.success = return_code == 0
            if not migration_execution_result.success:
                LOGGER.error("The migration script '%s' returned %d", migration_file_path, return_code)

        return migration_execution_result

    class MigrationScriptReturnCodeNotZeroException(SymigrateException):
        pass
