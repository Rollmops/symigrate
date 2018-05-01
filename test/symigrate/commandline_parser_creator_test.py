import os
import unittest
from io import StringIO

from symigrate.commandline_parser_creator import CommandlineParserCreator
from test.symigrate.helper import dedent_and_remove_first_empty_line


class CommandlineParserCreatorTestCase(unittest.TestCase):
    def test_help_output(self):
        os.environ["SYMIGRATE_MIGRATION_PATH"] = "/path"
        os.environ["SYMIGRATE_DB_FILE_PATH"] = "/db-path"
        commandline_parser_creator = CommandlineParserCreator()
        parser = commandline_parser_creator.create()

        out_stream = StringIO()
        parser.print_help(file=out_stream)

        out_stream_string = out_stream.getvalue()

        expected_help_output = dedent_and_remove_first_empty_line(
            """
            positional arguments:
              {info,migrate,diff}
                info                Show migration info
                migrate             Execute migration
                diff                Show difference of a modified migration script
            
            optional arguments:
              -h, --help            show this help message and exit
              --migration-path MIGRATION_PATH
                                    Migration directory path (default: /path). Environment
                                    variable: SYMIGRATE_MIGRATION_PATH
              --db-file-path DB_FILE_PATH
                                    The path to the migration database file (default: /db-
                                    path). Environment variable: SYMIGRATE_DB_FILE_PATH
              --scope SCOPE         The migration scope (default: DEFAULT). Environment
                                    variable: SYMIGRATE_SCOPE
              --migration-prefix MIGRATION_PREFIX
                                    The migration file name prefix (default: V).
                                    Environment variable: SYMIGRATE_MIGRATION_PREFIX
              --migration-separator MIGRATION_SEPARATOR
                                    The migration file name separator (default: __).
                                    Environment variable: SYMIGRATE_MIGRATION_SEPARATOR
              --migration-suffix MIGRATION_SUFFIX
                                    The migration file name suffix (default: None).
                                    Environment variable: SYMIGRATE_MIGRATION_SUFFIX
              --encoding ENCODING   The encoding used to read migration files (default:
                                    utf-8). Environment variable: SYMIGRATE_ENCODING
              --logging-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                                    Logging level (default: INFO). Environment variable:
                                    SYMIGRATE_LOGGING_LEVEL
              --logging-format LOGGING_FORMAT
                                    Change the logging format (default: %(levelname)s:
                                    %(message)s). Environment variable:
                                    SYMIGRATE_LOGGING_FORMAT
            """
        )

        self.assertIn(expected_help_output, out_stream_string)
