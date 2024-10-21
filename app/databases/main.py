import asyncpg
from app.settings import db_settings, com_settings


class Database:
    async def __aenter__(self):
        self.connection = await asyncpg.connect(
            user=db_settings.user_name,
            password=db_settings.user_password,
            host=db_settings.ip_address,
            port=db_settings.ip_port,
            database=db_settings.name,
            server_settings={
                "application_name": com_settings.APPLICATION_NAME,
                "jit": "off",
            },
            statement_cache_size=0,
        )
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()
