import uuid
from datetime import datetime


class Migration:
    def __init__(
            self, version: str,
            description: str,
            status: str,
            stdout: str,
            stderr: str,
            checksum: str,
            script: str,
            timestamp: datetime = None,
            scope: str = "DEFAULT",
            id: str = None
    ):
        self.version = version
        self.description = description
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        self.checksum = checksum
        self.script = script
        self.timestamp = timestamp or datetime.now()
        self.scope = scope
        self.id = id or self.create_uuid()

    @staticmethod
    def create_uuid():
        return str(uuid.uuid4()).replace("-", "")
