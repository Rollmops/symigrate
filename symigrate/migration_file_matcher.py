import re
from collections import namedtuple
from typing import Union


class MigrationFileMatcher:
    MatchResult = namedtuple("MatchResult", ["filename", "version", "description"])

    def __init__(self, prefix: str, separator: str, suffix: str):
        self.prefix = prefix
        self.separator = separator
        self.suffix = suffix

    def match(self, filename: str) -> Union[MatchResult, None]:
        pattern = self._create_pattern()

        match = re.match(pattern, filename)
        if match is not None:
            description = match.group(2).replace("_", " ")
            return MigrationFileMatcher.MatchResult(
                filename=filename,
                version=match.group(1),
                description=description
            )

    def _create_pattern(self):
        pattern = r"^{prefix}(\S+){separator}(\S+){suffix}$".format(
            prefix=self.prefix,
            separator=self.separator,
            suffix=self.suffix.replace(".", "\.")
        )
        return pattern
