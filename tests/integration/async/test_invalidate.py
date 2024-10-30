from surrpy import AsycSurrealDB
import pytest
from tests.integration.url import Url
import asyncio


class TestInvalidate:
    def setup_method(self):
        self.connection = AsycSurrealDB(Url().url)

    async def login(self, username: str, password: str):
        await self.connection.connect()
        outcome = await self.connection.signin(
            {
                "username": username,
                "password": password,
            }
        )
        return outcome

    def teardown_method(self):
        async def teardown_queries():
            for query in self.queries:
                await self.connection.query(query)

        asyncio.run(teardown_queries())

    @pytest.mark.skip(reason="IDK what invalidate does")
    def test_invalidate(self):
        self.queries = ["DELETE user;"]

        async def run():
            await self.login("root", "root")
            await self.connection.query("CREATE user:tobie SET name = 'Tobie';")
            await self.connection.query("CREATE user:jaime SET name = 'Jaime';")

            outcome = await self.connection.query("SELECT * FROM user;")
            assert [
                {"id": "user:jaime", "name": "Jaime"},
                {"id": "user:tobie", "name": "Tobie"},
            ] == outcome

            await self.connection.invalidate()
            outcome = await self.connection.query("SELECT * FROM user;")
            assert [
                {"id": "user:jaime", "name": "Jaime"},
                {"id": "user:tobie", "name": "Tobie"},
            ] == outcome

        asyncio.run(run())
