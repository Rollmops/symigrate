import os


class MigrationScriptChecker:
    @staticmethod
    def check(file_path: str):
        MigrationScriptChecker._check_permissions(file_path)

    @staticmethod
    def _check_permissions(file_path: str):
        if not os.access(file_path, os.X_OK):
            raise MigrationScriptChecker.MigrationScriptPermissionException(
                "Migration script '{file_path}' is not executable".format(file_path=file_path)
            )

    class MigrationScriptPermissionException(Exception):
        pass
