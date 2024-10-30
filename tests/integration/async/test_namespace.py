from typing import List
from unittest import TestCase, main

from surrpy import AsycSurrealDB
from tests.integration.url import Url
import asyncio


class TestNamespace:
    def setup_method(self):
        self.connection = AsycSurrealDB(Url().url)
        self.queries: List[str] = []

    def teardown_method(self):
        async def teardown_queries():
            for query in self.queries:
                await self.connection.query(query)

        asyncio.run(teardown_queries())

    def test_namespace(self):
        async def namespace():
            await self.connection.connect()
            _ = await self.connection.use_database("test")
            _ = await self.connection.use_namespace("test")

        asyncio.run(namespace())

    def test_namespace_in_sequence(self):
        self.queries = ["DELETE user;"]

        async def namespace():
            await self.connection.connect()
            await self.connection.use_database("test")
            await self.connection.use_namespace("test")

            await self.connection.query("CREATE user:tobie SET name = 'Tobie';")
            await self.connection.query("CREATE user:jaime SET name = 'Jaime';")

            outcome = await self.connection.query("SELECT * FROM user;")
            assert [
                {"id": "user:jaime", "name": "Jaime"},
                {"id": "user:tobie", "name": "Tobie"},
            ] == outcome

            await self.connection.use_database("database")
            await self.connection.use_namespace("namespace")

            outcome = await self.connection.query("SELECT * FROM user;")
            assert [] == outcome

            await self.connection.use_database("test")
            await self.connection.use_namespace("test")

            outcome = await self.connection.query("SELECT * FROM user;")
            assert [
                {"id": "user:jaime", "name": "Jaime"},
                {"id": "user:tobie", "name": "Tobie"},
            ] == outcome

        asyncio.run(namespace())


if __name__ == "__main__":
    main()
