import sqlite3
import sys
from argparse import Namespace

from system_migrate.command.info_command import InfoCommand
from system_migrate.commandline_parser_creator import CommandlineParserCreator
from system_migrate.executed_migration_repository import ExecutedMigrationRepository
from system_migrate.migration_merge_service import MigrationMergeService
from system_migrate.migration_repository import MigrationRepository


class CommandlineParsePhase:
    def __init__(self):
        commandline_parser_creator = CommandlineParserCreator()
        self.parser = commandline_parser_creator.create()

    def start(self, args):
        commandline_arguments = self.parser.parse_args(args)

        interface_creation_phase = InterfaceCreationPhase(commandline_arguments)
        interface_creation_phase.start()


class InterfaceCreationPhase:
    def __init__(self, commandline_arguments: Namespace):
        self.commandline_arguments = commandline_arguments

    def start(self):
        database_connection = sqlite3.connect(self.commandline_arguments.db_path).cursor().connection

        main_phase = MainPhase(database_connection, self.commandline_arguments)
        main_phase.start()


class MainPhase:
    def __init__(self, database_connection: sqlite3.Connection, commandline_arguments: Namespace):
        self.commandline_arguments = commandline_arguments

        self.executed_migration_repository = ExecutedMigrationRepository(database_connection)
        migration_repository = MigrationRepository(commandline_arguments.migration_path)
        migration_merge_service = MigrationMergeService()

        self.info_command = InfoCommand(
            self.executed_migration_repository, migration_repository, migration_merge_service
        )

    def start(self):
        self.executed_migration_repository.init()

        if self.commandline_arguments.command == "info":
            self.info_command.run()


def main():
    commandline_parse_phase = CommandlineParsePhase()
    commandline_parse_phase.start(sys.argv[1:])


if __name__ == '__main__':
    main()
