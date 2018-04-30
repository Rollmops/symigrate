import logging
import subprocess
from datetime import datetime

from symigrate import SymigrateException
from symigrate.defaults import SYMIGRATE_MIGRATION_TIMEOUT, SYMIGRATE_ENCODING
from symigrate.migration_execution_result import MigrationExecutionResult

LOGGER = logging.getLogger(__name__)


class MigrationScriptRunner:
    def __init__(self, timeout: int = SYMIGRATE_MIGRATION_TIMEOUT, encoding: str = SYMIGRATE_ENCODING):
        self.timeout = timeout
        self.encoding = encoding

    def run_migration_script(self, migration_file_path: str) -> MigrationExecutionResult:
        LOGGER.info("Running migration script '%s'", migration_file_path)
        migration_execution_result = MigrationExecutionResult(
            execution_timestamp=datetime.now()
        )
        try:
            process = subprocess.Popen(migration_file_path, shell=True)
            process.wait(self.timeout)
        except Exception as exception:
            LOGGER.error(repr(exception))
            migration_execution_result.success = False
        else:
            LOGGER.debug("Migration script return code: %d", process.returncode)
            migration_execution_result.success = process.returncode == 0
            if not migration_execution_result.success:
                LOGGER.error("The migration script '%s' returned code %d", migration_file_path, process.returncode)

        return migration_execution_result

    class MigrationScriptReturnCodeNotZeroException(SymigrateException):
        pass
