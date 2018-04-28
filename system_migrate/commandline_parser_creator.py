import os
from argparse import ArgumentParser


class CommandlineParserCreator:

    @staticmethod
    def create():
        parser = ArgumentParser()
        parser.add_argument(
            "--migration-path", help="Migration directory path (default: %(default)s)", default=os.getcwd()
        )
        parser.add_argument(
            "--db-path", help="The path to the migration database file (default: %(default)s)",
            default=CommandlineParserCreator._get_default_database_path()
        )
        parser.add_argument(
            "--scope", help="The migration scope (default: %(default)s)", default="DEFAULT"
        )
        subparsers = parser.add_subparsers(dest="command")

        info_parser = subparsers.add_parser("info", help="Show migration info")

        return parser

    @staticmethod
    def _get_default_database_path():
        home_path = os.environ.get("HOME", os.getcwd())
        return os.path.join(home_path, ".migration.db")
