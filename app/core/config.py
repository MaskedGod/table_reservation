from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    test_db_host: str
    test_db_port: int
    test_db_user: str
    test_db_pass: str
    test_db_name: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def test_database_url(self):
        return f"postgresql+asyncpg://{self.test_db_user}:{self.test_db_pass}@{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"

    model_config = ConfigDict(env_file=".env")


db_settings = DatabaseSettings()
