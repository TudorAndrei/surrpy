"""
Tests the Update operation of the AsyncSurrealDB class with query and merge function.
"""

import asyncio
from typing import List
from unittest import TestCase, main

from surrpy import AsycSurrealDB
from tests.integration.url import Url


class TestAsyncHttpMerge:
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

    def test_merge_person_with_tags(self):
        self.queries = ["DELETE user;"]

        async def merge_active():
            await self.connection.query("CREATE user:tobie SET name = 'Tobie';")
            await self.connection.query("CREATE user:jaime SET name = 'Jaime';")

            _ = await self.connection.merge(
                "user",
                {
                    "active": True,
                },
            )
            assert [
                {"active": True, "id": "user:jaime", "name": "Jaime"},
                {"active": True, "id": "user:tobie", "name": "Tobie"},
            ] == await self.connection.query("SELECT * FROM user;")

        asyncio.run(merge_active())


if __name__ == "__main__":
    main()
