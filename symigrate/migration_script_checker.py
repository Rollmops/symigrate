import logging
import os

from symigrate import SymigrateException

LOGGER = logging.getLogger(__name__)


class MigrationScriptChecker:
    os_access_func_hook = os.access

    @staticmethod
    def check(file_path: str):
        MigrationScriptChecker._check_permissions(file_path)

    @staticmethod
    def _check_permissions(file_path: str):
        LOGGER.debug("Checking execution permissions for: %s", file_path)
        if not MigrationScriptChecker.os_access_func_hook(file_path, os.X_OK):
            raise MigrationScriptChecker.MigrationScriptPermissionException(
                "Migration script '{file_path}' is not executable".format(file_path=file_path)
            )

    class MigrationScriptPermissionException(SymigrateException):
        pass
