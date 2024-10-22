from pydantic import Field
from typing import Optional
from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    API_PATH: str = Field('/', title="FastAPI api path")
    APPLICATION_NAME: str = "arbitration"
    LOCAL: bool = Field(False, title="Локальный запуск")
    LOGGING_LEVEL: str = Field(..., title="Logging level")

    class Config:
        case_sensitive = False

#
# class DB(BaseSettings):
#     ip_address: str = Field(..., title="IP address")
#     ip_port: Optional[int] = Field(5432, title="Port")
#     name: str = Field(..., title="Namу database")
#     user_name: str = Field(..., title="Login")
#     user_password: str = Field(..., title="Password")
#     min_connections: Optional[int] = Field(1, title="Min connection")
#     max_connections: Optional[int] = Field(5, title="Max connection")
#     max_inactive_connection_lifetime: Optional[float] = Field(3600, title="Max time connection")
#
#     class Config:
#         env_prefix = "DB_"
#         case_sensitive = False


class TelegramBot(BaseSettings):
    NAME: str = Field(..., title="Name Bot")
    TOKEN: str = Field(..., title="Token Bot")
    TIMEOUT_REFRESH: Optional[int] = Field(10, title="Timeout Bot")

    class Config:
        env_prefix = 'TB_'
        case_sensitive = False

#
# class RedisSettings(BaseSettings):
#     ip_address: str = Field(..., title="IP address")
#     port: Optional[int] = Field(6379, title="Port")
#     login: str = Field(..., title="Login")
#     password: str = Field(..., title="Password")
#
#     class Config:
#         env_prefix = 'REDIS_'
#         case_sensitive = False



com_settings = CommonSettings()
# db_settings = DB()
tb_settings = TelegramBot()
# redis_settings = RedisSettings()


DATA_RUB = {"userId": 20275521, "tokenId": "USDT", "currencyId": "RUB", "payment": ["75", "379", "377"], "side": "1",
            "size": "50", "page": "1", "amount": "", "authMaker": False, "canTrade": False, "itemRegion": 2}

DATA_KZT = {"userId": 20275521, "tokenId": "USDT", "currencyId": "KZT", "payment": ["549"], "side": "1",
            "size": "50", "page": "1", "amount": "", "authMaker": False, "canTrade": False, "itemRegion": 2}



