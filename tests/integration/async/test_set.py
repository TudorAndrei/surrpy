"""
Tests the Set operation of the AsyncSurrealDB class.
"""

import asyncio
from typing import List
from unittest import TestCase, main

from surrpy import AsycSurrealDB
from tests.integration.url import Url


class TestAsyncSet:
    def setup_method(self):
        self.connection = AsycSurrealDB(Url().url)
        self.queries: List[str] = []

        async def login():
            await self.connection.connect()
            await self.connection.signin(
                {
                    "username": "root",
                    "password": "root",
                }
            )

        asyncio.run(login())

    def teardown_method(self):
        async def teardown_queries():
            for query in self.queries:
                await self.connection.query(query)

        asyncio.run(teardown_queries())

    def test_set_ql(self):
        self.queries = ["DELETE person;"]
        query = "CREATE person:100 SET name = 'Tobie', company = 'SurrealDB', skills = ['Rust', 'Go', 'JavaScript'];"

        async def set():
            outcome = await self.connection.query(query)
            assert [
                {
                    "id": "person:100",
                    "name": "Tobie",
                    "company": "surrpy",
                    "skills": ["Rust", "Go", "JavaScript"],
                }
            ] == outcome

        asyncio.run(set())

    def test_set(self):
        self.queries = ["DELETE person;"]
        query = "CREATE person:100 SET name = $name;"

        async def set():
            _ = await self.connection.set(
                "name",
                {
                    "name": "Tobie",
                    "last": "Morgan Hitchcock",
                },
            )
            _ = await self.connection.query(query)
            outcome = await self.connection.query("SELECT * FROM person;")
            assert [
                {
                    "id": "person:100",
                    "name": {"last": "Morgan Hitchcock", "name": "Tobie"},
                }
            ] == outcome

        asyncio.run(set())


if __name__ == "__main__":
    main()
