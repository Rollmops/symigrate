import unittest

from symigrate import __version__
from symigrate.main.symigrate import CommandlineParsePhase
from test.symigrate.helper import capture_output


class GlobalCommandsAcceptanceTestCase(unittest.TestCase):
    def test_version_printing(self):
        command_line_parser_phase = CommandlineParsePhase()
        with capture_output() as output:
            command_line_parser_phase.start(["--version"])

        self.assertEqual(f"{__version__}\n", output[0].getvalue())
