from typing import List
import asyncio

import pytest

from surrpy import AsycSurrealDB
from tests.integration.url import Url

loop: asyncio.AbstractEventLoop


@pytest.mark.asyncio(loop_scope="class")
class TestNamespace:
    username = "root"
    password = "root"
    connection = AsycSurrealDB(Url().url)

    def setup_method(self):
        self.queries: List[str] = []

        async def setup():
            await self.connection.connect()
            await self.connection.signin(
                {
                    "username": self.username,
                    "password": self.password,
                }
            )

        asyncio.get_event_loop().run_until_complete(setup())

    def teardown_method(self):
        async def teardown():
            for query in self.queries:
                await self.connection.query(query)

        asyncio.get_event_loop().run_until_complete(teardown())

    async def test_namespace(self):
        await self.connection.use_database("test")
        await self.connection.use_namespace("test")

    async def test_namespace_in_sequence(self):
        self.queries = ["DELETE user;"]

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
