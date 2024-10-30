"""This file defines the interface between python and the Rust surrpy library for logging in."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional
import json

from surrpy.errors import surrpyError
from surrpy.rust_surrpy import (
    rust_authenticate_future,
    rust_sign_in_future,
    rust_sign_up_future,
    rust_invalidate_future,
)

if TYPE_CHECKING:
    from surrpy.connection_interface import surrpy


class AsyncSignInMixin:
    """This class is responsible for the interface between python and the Rust surrpy library for logging in."""

    async def signin(self: surrpy, data: Optional[Dict[str, str]] = None) -> None:
        """
        Signs in to the database.

        :param password: the password to sign in with
        :param username: the username to sign in with

        :return: None
        """
        if data is None:
            data = {}
        data = {key.lower(): value for key, value in data.items()}

        password: str = data.get("password", data.get("pass", data.get("p", "root")))
        username: str = data.get("username", data.get("user", data.get("u", "root")))
        await rust_sign_in_future(self._connection, password, username)

    async def signup(
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

        return await rust_sign_up_future(
            self._connection, data, namespace, database, scope
        )

    async def authenticate(self: surrpy, jwt: str) -> bool:
        """
        Authenticates a JWT.

        :param jwt: the JWT to authenticate
        :return: None
        """
        try:
            return await rust_authenticate_future(self._connection, jwt)
        except Exception as e:
            raise surrpyError(e) from None

    async def invalidate(self: surrpy) -> None:
        """
        Invalidates a connection JWT.

        :return: None
        """
        try:
            return await rust_invalidate_future(self._connection)
        except Exception as e:
            raise surrpyError(e) from None
