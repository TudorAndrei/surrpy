"""This file defines the interface between python and the Rust surrpy library for logging in."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Dict, Optional

from surrpy.asyncio_runtime import AsyncioRuntime
from surrpy.errors import SurrealError
from surrpy.surrpy import (
    rust_authenticate_future,
    rust_sign_in_future,
    rust_sign_up_future,
    rust_invalidate_future,
)

if TYPE_CHECKING:
    from surrpy.connection_interface import surrpy


class SignInMixin:
    """This class is responsible for the interface between python and the Rust surrpy library for logging in."""

    def signin(self: surrpy, data: Optional[Dict[str, str]] = None) -> None:
        """
        Signs in to the database.

        :param password: the password to sign in with
        :param username: the username to sign in with

        :return: None
        """

        async def _signin(connection, password, username):
            return await rust_sign_in_future(connection, password, username)

        if data is None:
            data = {}
        data = {key.lower(): value for key, value in data.items()}

        password: str = data.get("password", data.get("pass", data.get("p", "root")))
        username: str = data.get("username", data.get("user", data.get("u", "root")))

        try:
            loop_manager = AsyncioRuntime()
            loop_manager.loop.run_until_complete(
                _signin(self._connection, password, username)
            )
        except Exception as e:
            raise SurrealError(e) from None

    def signup(
        self: surrpy,
        namespace: str,
        database: str,
        scope: str,
        data: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Signs up to an auth scope within a namespace and database.

        :param namespace: the namespace the auth scope is associated with
        :param database: the database the auth scope is associated with
        :param scope: the scope the auth scope is associated with
        :param data: the data to sign up with
        :return: an JWT for that auth scope
        """

        if data is None:
            data = {}
        data = json.dumps(data)

        async def _signup(connection, data, namespace, database, scope):
            return await rust_sign_up_future(
                connection, data, namespace, database, scope
            )

        try:
            loop_manager = AsyncioRuntime()
            return loop_manager.loop.run_until_complete(
                _signup(self._connection, data, namespace, database, scope)
            )
        except Exception as e:
            raise SurrealError(e) from None

    def authenticate(self: surrpy, jwt: str) -> bool:
        """
        Authenticates a JWT.

        :param jwt: the JWT to authenticate
        :return: None
        """

        async def _authenticate(connection, jwt):
            return await rust_authenticate_future(connection, jwt)

        try:
            loop_manager = AsyncioRuntime()
            return loop_manager.loop.run_until_complete(
                _authenticate(self._connection, jwt)
            )
        except Exception as e:
            raise SurrealError(e) from None

    def invalidate(self: surrpy) -> None:
        """
        Invalidates a connection JWT.

        :return: None
        """

        async def _invalidate(connection):
            return await rust_invalidate_future(connection)

        try:
            loop_manager = AsyncioRuntime()
            loop_manager.loop.run_until_complete(_invalidate(self._connection))
        except Exception as e:
            raise SurrealError(e) from None
