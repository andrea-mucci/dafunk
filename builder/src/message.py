from core.dafunk import DaEvent


class BuildRequestMessage(DaEvent):
    repository_name: str

class BuildResponseMessage(DaEvent):
    build_id: str
    status: str