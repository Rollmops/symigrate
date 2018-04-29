import os
from argparse import ArgumentParser

from symigrate.defaults import SYMIGRATE_ENCODING, SYMIGRATE_MIGRATION_SUFFIX, SYMIGRATE_MIGRATION_SEPARATOR, \
    SYMIGRATE_DEFAULT_SCOPE, SYMIGRATE_MIGRATION_PREFIX, SYMIGRATE_LOGGING_LEVEL


class CommandlineParserCreator:

    @staticmethod
    def create():
        parser = ArgumentParser()
        parser.add_argument(
            "--migration-path",
            help="Migration directory path (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_MIGRATION_PATH", os.getcwd())
        )
        parser.add_argument(
            "--db-file-path",
            help="The path to the migration database file (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_DB_FILE_PATH", CommandlineParserCreator._get_default_database_path())
        )
        parser.add_argument(
            "--scope",
            help="The migration scope (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_SCOPE", SYMIGRATE_DEFAULT_SCOPE)
        )
        parser.add_argument(
            "--migration-prefix",
            help="The migration file name prefix (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_MIGRATION_PREFIX", SYMIGRATE_MIGRATION_PREFIX)
        )
        parser.add_argument(
            "--migration-separator",
            help="The migration file name separator (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_MIGRATION_SEPARATOR", SYMIGRATE_MIGRATION_SEPARATOR)
        )
        parser.add_argument(
            "--migration-suffix",
            help="The migration file name suffix (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_MIGRATION_SUFFIX", SYMIGRATE_MIGRATION_SUFFIX)
        )
        parser.add_argument(
            "--encoding",
            help="The encoding used to read migration files (default: %(default)s)",
            default=SYMIGRATE_ENCODING
        )
        parser.add_argument(
            "--logging-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Logging level (default: %(default)s)",
            default=os.environ.get("SYMIGRATE_LOGGING_LEVEL", SYMIGRATE_LOGGING_LEVEL)
        )

        subparsers = parser.add_subparsers(dest="command")

        info_parser = subparsers.add_parser("info", help="Show migration info")
        migrate_parser = subparsers.add_parser("migrate", help="Execute migration")

        return parser

    @staticmethod
    def _get_default_database_path():
        home_path = os.environ.get("HOME", os.getcwd())
        return os.path.join(home_path, ".symigrate.db")
