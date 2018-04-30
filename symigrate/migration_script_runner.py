import logging
import subprocess
from datetime import datetime

from symigrate import SymigrateException
from symigrate.defaults import SYMIGRATE_MIGRATION_TIMEOUT
from symigrate.migration_execution_result import MigrationExecutionResult

LOGGER = logging.getLogger(__name__)


class MigrationScriptRunner:
    def __init__(self, timeout: int = SYMIGRATE_MIGRATION_TIMEOUT):
        self.timeout = timeout

    def run_migration_script(self, migration_file_path: str) -> MigrationExecutionResult:
        LOGGER.info("Running migration script '%s'", migration_file_path)
        migration_execution_result = MigrationExecutionResult(
            stdout="",
            stderr="",
            execution_timestamp=datetime.now()
        )
        try:
            process = subprocess.Popen(
                migration_file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            process.wait(self.timeout)
        except Exception as exception:
            LOGGER.error(repr(exception))
            migration_execution_result.success = False
        else:
            LOGGER.debug("Migration script return code: %d", process.returncode)
            self._set_migration_execution_result(migration_execution_result, process)
            if not migration_execution_result.success:
                LOGGER.error("The migration script '%s' returned %d", migration_file_path, process.returncode)

        return migration_execution_result

    @staticmethod
    def _set_migration_execution_result(migration_execution_result, process):
        migration_execution_result.success = process.returncode == 0
        migration_execution_result.stdout = process.stdout.read().decode()
        migration_execution_result.stderr = process.stderr.read().decode()

    class MigrationScriptReturnCodeNotZeroException(SymigrateException):
        pass
