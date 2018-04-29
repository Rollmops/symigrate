import os
import sqlite3
import unittest
from io import StringIO

from symigrate.main.symigrate import CommandlineParsePhase, InterfaceCreationPhase, MainPhase


class InfoCommandAcceptanceTestCase(unittest.TestCase):

    def setUp(self):
        self.migrations_path = os.path.join(os.path.dirname(__file__), "data", "migrations")
        self.assertTrue(os.path.isdir(self.migrations_path))

        self.database_connection = sqlite3.connect(":memory:")
        self.out_stream = StringIO()
        InterfaceCreationPhase.database_connection_hook = self.database_connection
        MainPhase.out_stream_hook = self.out_stream

    def test_info_no_scope(self):
        commandline_parse_phase = CommandlineParsePhase()

        commandline_parse_phase.start(["--migration-path", self.migrations_path, "info"])

        expected_output = (
            "Scope: DEFAULT\n"
            "+-----------+-------------------+----------+\n"
            "| Version   | Description       | Status   |\n"
            "+===========+===================+==========+\n"
            "| 1.0.0     | test migration    | PENDING  |\n"
            "+-----------+-------------------+----------+\n"
            "| 1.1.0     | another migration | PENDING  |\n"
            "+-----------+-------------------+----------+\n"
        )

        self.assertEqual(expected_output, self.out_stream.getvalue())

    def test_info_custom_scope(self):
        commandline_parse_phase = CommandlineParsePhase()

        commandline_parse_phase.start(["--migration-path", self.migrations_path, "--scope", "my_scope", "info"])

        expected_output = (
            "Scope: my_scope\n"
            "+-----------+-------------------+----------+\n"
            "| Version   | Description       | Status   |\n"
            "+===========+===================+==========+\n"
            "| 1.0.0     | test migration    | PENDING  |\n"
            "+-----------+-------------------+----------+\n"
            "| 1.1.0     | another migration | PENDING  |\n"
            "+-----------+-------------------+----------+\n"
        )

        self.assertEqual(expected_output, self.out_stream.getvalue())
