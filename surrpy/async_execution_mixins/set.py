"""This file defines the interface between python and the Rust surrpy library for setting a key value."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from surrpy.errors import surrpyError
from surrpy.rust_surrpy import rust_set_future

if TYPE_CHECKING:
    from surrpy.connection_interface import surrpy


class AsyncSetMixin:
    """This class is responsible for the interface between python and the Rust surrpy library for creating a document."""

    async def set(self: surrpy, key: str, value: dict) -> None:
        """
        Creates a new document in the database.

        :param name: the name of the document to create
        :param data: the data to store in the document

        :return: None
        """
        json_str = None
        try:
            json_str = json.dumps(value)
        except json.JSONEncodeError as e:
            print(f"cannot serialize value {type(value)} to json")
            raise surrpyError(e) from None

        if json_str is not None:
            try:
                _ = await rust_set_future(self._connection, key, json.dumps(value))
            except Exception as e:
                raise surrpyError(e) from None
