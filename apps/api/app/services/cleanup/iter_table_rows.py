from collections.abc import Iterator
from typing import Any

from appwrite.query import Query

from app.constants.paging import PAGE_SIZE
from app.core.config import settings
from app.services.appwrite.get_tables_db import get_tables_db


def iter_table_rows(table_id: str, model_type: type) -> Iterator[Any]:
    """Walk through every row of a table, one page at a time. Read-only."""
    tables = get_tables_db()
    last_id = None
    while True:
        queries = [Query.limit(PAGE_SIZE)]
        if last_id:
            queries.append(Query.cursor_after(last_id))
        rows = tables.list_rows(
            database_id=settings.appwrite_database_id,
            table_id=table_id,
            queries=queries,
            model_type=model_type,
        ).rows
        yield from rows
        if len(rows) < PAGE_SIZE:
            return
        last_id = rows[-1].id
