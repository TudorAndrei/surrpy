"""
Tests the Update operation of the AsyncSurrealDB class with query and update function.
"""

from typing import List
from unittest import TestCase, main

from surrpy import SurrealDB
from tests.integration.url import Url


class TestAsyncHttpUpdate:
    def setup_method(self):
        self.connection = SurrealDB(Url().url)
        self.queries: List[str] = []

        self.connection.signin(
            {
                "username": "root",
                "password": "root",
            }
        )

    def teardown_method(self):
        for query in self.queries:
            self.connection.query(query)

    def test_update_ql(self):
        self.queries = ["DELETE user;"]
        self.connection.query("CREATE user:tobie SET name = 'Tobie';")
        self.connection.query("CREATE user:jaime SET name = 'Jaime';")
        outcome = self.connection.query(
            "UPDATE user SET lastname = 'Morgan Hitchcock';"
        )
        assert [
            {"id": "user:jaime", "lastname": "Morgan Hitchcock", "name": "Jaime"},
            {"id": "user:tobie", "lastname": "Morgan Hitchcock", "name": "Tobie"},
        ] == outcome

    def test_update_person_with_tags(self):
        self.queries = ["DELETE person;"]
        _ = self.connection.query(
            """
            CREATE person:`失败` CONTENT
            {
                "user": "me",
                "pass": "*æ失败",
                "really": True,
                "tags": ["python", "documentation"],
            };
            """
        )

        outcome = self.connection.update(
            "person:`失败`",
            {
                "user": "still me",
                "pass": "*æ失败",
                "really": False,
                "tags": ["python", "test"],
            },
        )
        assert {
            "id": "person:⟨失败⟩",
            "user": "still me",
            "pass": "*æ失败",
            "really": False,
            "tags": ["python", "test"],
        } == outcome


if __name__ == "__main__":
    main()
