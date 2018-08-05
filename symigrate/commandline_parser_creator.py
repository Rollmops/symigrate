import os
from argparse import ArgumentParser

from symigrate import __description__
from symigrate.defaults import SYMIGRATE_ENCODING, SYMIGRATE_MIGRATION_SUFFIX, SYMIGRATE_MIGRATION_SEPARATOR, \
    SYMIGRATE_DEFAULT_SCOPE, SYMIGRATE_MIGRATION_PREFIX, SYMIGRATE_LOGGING_LEVEL, SYMIGRATE_MIGRATION_TIMEOUT


class CommandlineParserCreator:

    @staticmethod
    def create():
        parser = ArgumentParser(description=__description__)
        CommandlineParserCreator._setup_global_parser(parser)

        subparsers = parser.add_subparsers(dest="command")
        CommandlineParserCreator._setup_info_parser(subparsers)
        CommandlineParserCreator._setup_migrate_parser(subparsers)
        CommandlineParserCreator._setup_diff_parser(subparsers)

        return parser

    @staticmethod
    def _setup_diff_parser(subparsers):
        diff_parser = subparsers.add_parser("diff", help="Show difference of a modified migration script")
        diff_parser.add_argument(
            "-v", "--version",
            help="The version that should be compared",
            required=True
        )

    @staticmethod
    def _setup_info_parser(subparsers):
        subparsers.add_parser("info", help="Show migration info")

    @staticmethod
    def _setup_global_parser(parser):
        parser.add_argument("--version", help="Print the version information to stdout", action="store_true")
        parser.add_argument(
            "--migration-path",
            help="Migration directory path (default: %(default)s). "
                 "Environment variable: SYMIGRATE_MIGRATION_PATH",
            default=os.environ.get("SYMIGRATE_MIGRATION_PATH", os.getcwd())
        )
        parser.add_argument(
            "--db-file-path",
            help="The path to the migration database file (default: %(default)s). "
                 "Environment variable: SYMIGRATE_DB_FILE_PATH",
            default=os.environ.get("SYMIGRATE_DB_FILE_PATH", CommandlineParserCreator._get_default_database_path())
        )
        parser.add_argument(
            "--scope",
            help="The migration scope (default: %(default)s). "
                 "Environment variable: SYMIGRATE_SCOPE",
            default=os.environ.get("SYMIGRATE_SCOPE", SYMIGRATE_DEFAULT_SCOPE)
        )
        parser.add_argument(
            "--migration-prefix",
            help="The migration file name prefix (default: %(default)s). "
                 "Environment variable: SYMIGRATE_MIGRATION_PREFIX",
            default=os.environ.get("SYMIGRATE_MIGRATION_PREFIX", SYMIGRATE_MIGRATION_PREFIX)
        )
        parser.add_argument(
            "--migration-separator",
            help="The migration file name separator (default: %(default)s). "
                 "Environment variable: SYMIGRATE_MIGRATION_SEPARATOR",
            default=os.environ.get("SYMIGRATE_MIGRATION_SEPARATOR", SYMIGRATE_MIGRATION_SEPARATOR)
        )
        parser.add_argument(
            "--migration-suffix",
            help="The migration file name suffix (default: %(default)s). "
                 "Environment variable: SYMIGRATE_MIGRATION_SUFFIX",
            default=os.environ.get("SYMIGRATE_MIGRATION_SUFFIX", SYMIGRATE_MIGRATION_SUFFIX)
        )
        parser.add_argument(
            "--encoding",
            help="The encoding used to read migration files (default: %(default)s). "
                 "Environment variable: SYMIGRATE_ENCODING",
            default=os.environ.get("SYMIGRATE_ENCODING", SYMIGRATE_ENCODING)
        )
        parser.add_argument(
            "--logging-level",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Logging level (default: %(default)s). "
                 "Environment variable: SYMIGRATE_LOGGING_LEVEL",
            default=os.environ.get("SYMIGRATE_LOGGING_LEVEL", SYMIGRATE_LOGGING_LEVEL)
        )
        parser.add_argument(
            "--logging-format",
            help="Change the logging format (default: %(default)s). "
                 "Environment variable: SYMIGRATE_LOGGING_FORMAT",
            default=os.environ.get("SYMIGRATE_LOGGING_FORMAT", "%(levelname)s: %(message)s")
        )

    @staticmethod
    def _setup_migrate_parser(subparsers):
        migrate_parser = subparsers.add_parser("migrate", help="Execute migration")
        migrate_parser.add_argument("--single", help="Only execute the next pending migration", action="store_true")
        migrate_parser.add_argument(
            "--timeout",
            help="Timeout in seconds for migration scripts (default: %(default)s). "
                 "Environment variable: SYMIGRATE_MIGRATION_TIMEOUT",
            default=os.environ.get("SYMIGRATE_MIGRATION_TIMEOUT", SYMIGRATE_MIGRATION_TIMEOUT),
            type=int
        )

    @staticmethod
    def _get_default_database_path():
        home_path = os.environ.get("HOME", os.getcwd())
        return os.path.join(home_path, ".symigrate.db")
