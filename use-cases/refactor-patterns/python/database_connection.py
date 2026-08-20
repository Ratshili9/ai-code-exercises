from abc import ABC, abstractmethod
from typing import Optional, Any


class DatabaseStrategy(ABC):
    """Abstract Strategy interface for different database connection strategies."""
    
    @abstractmethod
    def build_connection_string(self, config: 'DatabaseConnection') -> str:
        """Constructs and returns the database-specific connection URI or identifier."""
        pass


class MySQLStrategy(DatabaseStrategy):
    def build_connection_string(self, config: 'DatabaseConnection') -> str:
        conn_str = f"mysql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
        conn_str += f"?charset={config.charset}"
        conn_str += f"&connectionTimeout={config.connection_timeout}"
        if config.use_ssl:
            conn_str += "&useSSL=true"
        print(f"MySQL Connection: {conn_str}")
        return conn_str


class PostgreSQLStrategy(DatabaseStrategy):
    def build_connection_string(self, config: 'DatabaseConnection') -> str:
        conn_str = f"postgresql://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
        if config.use_ssl:
            conn_str += "?sslmode=require"
        print(f"PostgreSQL Connection: {conn_str}")
        return conn_str


class MongoDBStrategy(DatabaseStrategy):
    def build_connection_string(self, config: 'DatabaseConnection') -> str:
        conn_str = f"mongodb://{config.username}:{config.password}@{config.host}:{config.port}/{config.database}"
        conn_str += f"?retryAttempts={config.retry_attempts}"
        conn_str += f"&poolSize={config.pool_size}"
        if config.use_ssl:
            conn_str += "&ssl=true"
        print(f"MongoDB Connection: {conn_str}")
        return conn_str


class RedisStrategy(DatabaseStrategy):
    def build_connection_string(self, config: 'DatabaseConnection') -> str:
        conn_str = f"{config.host}:{config.port}/{config.database}"
        print(f"Redis Connection: {conn_str}")
        return conn_str


class DatabaseStrategyFactory:
    """Factory creating appropriate DatabaseStrategy instances based on db_type."""
    _strategies = {
        'mysql': MySQLStrategy,
        'postgresql': PostgreSQLStrategy,
        'mongodb': MongoDBStrategy,
        'redis': RedisStrategy
    }

    @classmethod
    def get_strategy(cls, db_type: str) -> DatabaseStrategy:
        strategy_class = cls._strategies.get(db_type.lower() if db_type else '')
        if not strategy_class:
            raise ValueError(f"Unsupported database type: {db_type}")
        return strategy_class()


class DatabaseConnection:
    """Database connection manager refactored with Strategy and Factory patterns."""
    def __init__(self, db_type, host, port, username, password, database,
                 use_ssl=False, connection_timeout=30, retry_attempts=3,
                 pool_size=5, charset='utf8'):
        self.db_type = db_type
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.use_ssl = use_ssl
        self.connection_timeout = connection_timeout
        self.retry_attempts = retry_attempts
        self.pool_size = pool_size
        self.charset = charset
        self.connection = None

    def connect(self):
        print(f"Connecting to {self.db_type} database...")
        strategy = DatabaseStrategyFactory.get_strategy(self.db_type)
        strategy.build_connection_string(self)
        print("Connection successful!")
        return self.connection


if __name__ == "__main__":
    mysql_db = DatabaseConnection(
        db_type='mysql',
        host='localhost',
        port=3306,
        username='db_user',
        password='password123',
        database='app_db',
        use_ssl=True
    )
    mysql_db.connect()

    mongo_db = DatabaseConnection(
        db_type='mongodb',
        host='mongodb.example.com',
        port=27017,
        username='mongo_user',
        password='mongo123',
        database='analytics',
        pool_size=10,
        retry_attempts=5
    )
    mongo_db.connect()