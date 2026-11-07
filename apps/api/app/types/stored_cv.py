from dataclasses import dataclass


@dataclass
class StoredCV:
    row_id: str
    file_name: str | None
    text: str
