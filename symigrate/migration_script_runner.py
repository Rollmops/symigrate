import logging
import subprocess
from datetime import datetime
from typing import Union, Tuple

from symigrate.defaults import SYMIGRATE_SCRIPT_EXECUTION_TIMEOUT
from symigrate.migration_execution_result import MigrationExecutionResult

LOGGER = logging.getLogger(__name__)


class MigrationScriptRunner:
    def __init__(self, timeout: int = SYMIGRATE_SCRIPT_EXECUTION_TIMEOUT):
        self.timeout = timeout

    def run_migration_script(self, migration_file_path: str) -> Union[Tuple[bool, MigrationExecutionResult], None]:
        try:
            process = subprocess.Popen(migration_file_path)
        except PermissionError:
            LOGGER.error("Unable to run migration script '%s'. Please check permissions.", migration_file_path)
        else:

            try:
                outs, errs = process.communicate(timeout=self.timeout)
            except subprocess.TimeoutExpired:
                LOGGER.error("Migration script '%s' took more than %d seconds", migration_file_path, self.timeout)
                process.kill()
                outs, errs = process.communicate()

            migration_execution_result = MigrationExecutionResult(
                stdout=outs, stderr=errs, execution_timestamp=datetime.now()
            )
            return migration_execution_result
