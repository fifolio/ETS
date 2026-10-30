from typing import TypedDict


class CVRowData(TypedDict):
    userId: str
    fileId: str
    fileName: str
    text: str
