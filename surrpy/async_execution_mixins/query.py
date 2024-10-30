"""
This file defines the interface between python and the Rust surrpy library for querying the database.
queries can be found in the link below:
https://github.com/surrpy/surrpy/blob/main/lib/tests/fetch.rs.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, List, Union

from surrpy.errors import surrpyError
from surrpy.rust_surrpy import (
    rust_query_future,
    rust_select_future,
)

if TYPE_CHECKING:
    from surrpy.connection_interface import surrpy


class AsyncQueryMixin:
    """This class is responsible for the interface between python and the Rust surrpy library for creating a document."""

    async def query(self: surrpy, query: str) -> List[dict]:
        """
        queries the database.

        :param query: the query to run on the database

        :return: None
        """
        try:
            return json.loads(await rust_query_future(self._connection, query))[0]
        except Exception as e:
            raise surrpyError(e) from None

    async def select(self: surrpy, resource: str) -> Union[List[dict], dict]:
        """
        Performs a select query on the database for a particular resource.

        :param resource: the resource to select from

        :return: the result of the select
        """
        return await rust_select_future(self._connection, resource)
