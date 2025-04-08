from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """
    Конфигурация базы данных.

    Этот класс используется для загрузки настроек базы данных из переменных окружения
    или файла `.env`. Он предоставляет URL-адреса для подключения к основной базе данных
    и тестовой базе данных.

    Атрибуты:
        db_host (str): Хост основной базы данных.
        db_port (int): Порт основной базы данных.
        db_user (str): Имя пользователя для основной базы данных.
        db_pass (str): Пароль для основной базы данных.
        db_name (str): Имя основной базы данных.
        test_db_host (str): Хост тестовой базы данных.
        test_db_port (int): Порт тестовой базы данных.
        test_db_user (str): Имя пользователя для тестовой базы данных.
        test_db_pass (str): Пароль для тестовой базы данных.
        test_db_name (str): Имя тестовой базы данных.

    Методы:
        database_url: Возвращает URL для подключения к основной базе данных.
        test_database_url: Возвращает URL для подключения к тестовой базе данных.
    """

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
        """
        Возвращает URL для подключения к основной базе данных.

        Формат: postgresql+asyncpg://db_user:db_pass@db_host:db_port/db_name

        Returns:
            str: URL для подключения к основной базе данных.
        """
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def test_database_url(self) -> str:
        """
        Возвращает URL для подключения к тестовой базе данных.

        Формат: postgresql+asyncpg://test_db_user:test_db_pass@test_db_host:test_db_port/test_db_name

        Returns:
            str: URL для подключения к тестовой базе данных.
        """
        return f"postgresql+asyncpg://{self.test_db_user}:{self.test_db_pass}@{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"

    model_config = ConfigDict(env_file=".env")
    """
    Конфигурация модели Pydantic.

    Загружает переменные окружения из файла `.env`.
    """


db_settings = DatabaseSettings()
