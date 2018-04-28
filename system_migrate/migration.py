import uuid


class Migration:
    def __init__(
            self, version: str,
            description: str,
            status: str,
            checksum: str,
            script: str,
            scope: str = "DEFAULT",
            id: str = None
    ):
        self.version = version
        self.description = description
        self.status = status
        self.checksum = checksum
        self.script = script
        self.scope = scope
        self.id = id or self.create_uuid()

    @staticmethod
    def create_uuid():
        return str(uuid.uuid4()).replace("-", "")
