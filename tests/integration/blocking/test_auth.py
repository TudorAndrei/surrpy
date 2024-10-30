"""
Handles the integration tests for logging into the database using blocking operations.
"""

import pytest
import os
from unittest import TestCase, main

from surrpy import SurrealDB
from surrpy.errors import SurrealError
from tests.integration.url import Url


class TestAuth:
    def setup_method(self):
        self.connection = SurrealDB(Url().url)

    def teardown_method(self):
        pass

    def login(self, username: str, password: str) -> None:
        self.connection.signin(
            {
                "username": username,
                "password": password,
            }
        )

    def test_login_success(self):
        self.login("root", "root")

    def test_login_wrong_password(self):
        with pytest.raises(SurrealError) as context:
            self.login("root", "wrong")

        assert (
            True == "There was a problem with authentication" in str(context.exception)
        )

    def test_login_wrong_username(self):
        with pytest.raises(SurrealError) as context:
            self.login("wrong", "root")

        assert (
            True == "There was a problem with authentication" in str(context.exception)
        )


if __name__ == "__main__":
    main()
