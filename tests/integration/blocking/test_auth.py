"""
Handles the integration tests for logging into the database using blocking operations.
"""

import os
from unittest import TestCase, main

from surrealdb import surrealdb
from surrealdb.errors import surrealdbError
from tests.integration.url import Url


class TestAuth(TestCase):
    def setUp(self):
        self.connection = surrealdb(Url().url)

    def tearDown(self):
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
        with self.assertRaises(surrealdbError) as context:
            self.login("root", "wrong")

        self.assertEqual(
            True, "There was a problem with authentication" in str(context.exception)
        )

    def test_login_wrong_username(self):
        with self.assertRaises(surrealdbError) as context:
            self.login("wrong", "root")

        self.assertEqual(
            True, "There was a problem with authentication" in str(context.exception)
        )


if __name__ == "__main__":
    main()
