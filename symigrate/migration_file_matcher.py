import re
from collections import namedtuple
from typing import Union


class MigrationFileMatcher:
    MatchResult = namedtuple("MatchResult", ["filename", "version", "description"])

    def __init__(self, prefix: str, separator: str, suffix: str):
        self.prefix = prefix
        self.separator = separator
        self.suffix = ".*" if suffix is None else suffix.replace(".", "\.")

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
        pattern = r"^{prefix}(\S+){separator}([a-zA-Z0-9_]+){suffix}$".format(
            prefix=self.prefix,
            separator=self.separator,
            suffix=self.suffix
        )
        return pattern
