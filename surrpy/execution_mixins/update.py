"""This file defines the interface between python and the Rust surrpy library for updating rows in the database."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, List, Union

from surrpy.asyncio_runtime import AsyncioRuntime
from surrpy.errors import SurrealError
from surrpy.surrpy import (
    rust_merge_future,
    rust_patch_future,
    rust_update_future,
)

if TYPE_CHECKING:
    from surrpy.connection_interface import surrpy


class UpdateMixin:
    """This class is responsible for the interface between python and the Rust surrpy library for creating a document."""

    def update(self: surrpy, resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Updates the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to update the resource with
        :return: the updated resource such as an individual row or a list of rows
        """

        async def _update(connection, resource, data):
            return await rust_update_future(connection, resource, data)

        try:
            loop_manager = AsyncioRuntime()
            return json.loads(
                loop_manager.loop.run_until_complete(
                    _update(self._connection, resource, json.dumps(data))
                )
            )
        except Exception as e:
            raise SurrealError(e) from None

    def merge(self: surrpy, resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Merges the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to merge the resource with
        :return: the updated resource such as an individual row or a list of rows
        """

        async def _merge(connection, resource, data):
            return await rust_merge_future(connection, resource, data)

        try:
            loop_manager = AsyncioRuntime()
            return json.loads(
                loop_manager.loop.run_until_complete(
                    _merge(self._connection, resource, json.dumps(data))
                )
            )
        except Exception as e:
            raise SurrealError(e) from None

    def patch(self: surrpy, resource: str, data: dict) -> Union[List[dict], dict]:
        """
        Patches the given resource with the given data.

        :param resource: the resource to update
        :param data: the data to patch the resource with
        :return: the updated resource such as an individual row or a list of rows
        """

        async def _patch(connection, resource, data):
            return await rust_patch_future(connection, resource, data)

        try:
            loop_manager = AsyncioRuntime()
            return json.loads(
                loop_manager.loop.run_until_complete(
                    _patch(self._connection, resource, json.dumps(data))
                )
            )
        except Exception as e:
            raise SurrealError(e) from None
