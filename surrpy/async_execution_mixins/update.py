"""This file defines the interface between python and the Rust surrpy library for updating rows in the database."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, List, Union

from surrpy.errors import SurrealError
from surrpy.surrpy import (
    rust_merge_future,
    rust_patch_future,
    rust_update_future,
)

if TYPE_CHECKING:
    from surrpy.connection_interface import surrpy


class AsyncUpdateMixin:
    """This class is responsible for the interface between python and the Rust surrpy library for creating a document."""

    async def update(
        self: surrpy, resource: str, data: dict
    ) -> Union[List[dict], dict]:
        """
        Updates the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to update the resource with
        :return: the updated resource such as an individual row or a list of rows
        """
        try:
            return json.loads(
                await rust_update_future(self._connection, resource, json.dumps(data))
            )
        except Exception as e:
            raise SurrealError(e) from None

    async def merge(self: surrpy, resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Merges the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to merge the resource with
        :return: the updated resource such as an individual row or a list of rows
        """
        try:
            return json.loads(
                await rust_merge_future(self._connection, resource, json.dumps(data))
            )
        except Exception as e:
            raise SurrealError(e) from None

    async def patch(self: surrpy, resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Patches the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to patch the resource with
        :return: the updated resource such as an individual row or a list of rows
        """
        try:
            return json.loads(
                await rust_patch_future(self._connection, resource, json.dumps(data))
            )
        except Exception as e:
            raise SurrealError(e) from None
