"""
Handles the integration tests for logging into the database.
"""

import asyncio
import os
from unittest import TestCase, main

import pytest

from surrpy import AsycSurrealDB
from tests.integration.url import Url


class TestAsyncAuth:
    def setup_method(self):
        self.connection = AsycSurrealDB(Url().url)

    def teardown_method(self):
        pass

    async def login(self, username: str, password: str):
        await self.connection.connect()
        outcome = await self.connection.signin(
            {
                "username": username,
                "password": password,
            }
        )
        return outcome

    def test_login_success(self):
        outcome = asyncio.run(self.login("root", "root"))
        assert None is outcome

    def test_login_wrong_password(self):
        with pytest.raises(RuntimeError) as context:
            asyncio.run(self.login("root", "wrong"))

        assert (
            True == "There was a problem with authentication" in str(context.exception)
        )

    def test_login_wrong_username(self):
        with pytest.raises(RuntimeError) as context:
            asyncio.run(self.login("wrong", "root"))

        assert (
            True == "There was a problem with authentication" in str(context.exception)
        )


if __name__ == "__main__":
    main()
