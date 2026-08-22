import unittest
from database_connection import DatabaseConnection, DatabaseStrategyFactory, MySQLStrategy, PostgreSQLStrategy, MongoDBStrategy, RedisStrategy

class TestDatabaseConnectionRefactoring(unittest.TestCase):
    def test_factory_strategies(self):
        self.assertIsInstance(DatabaseStrategyFactory.get_strategy("mysql"), MySQLStrategy)
        self.assertIsInstance(DatabaseStrategyFactory.get_strategy("postgresql"), PostgreSQLStrategy)
        self.assertIsInstance(DatabaseStrategyFactory.get_strategy("mongodb"), MongoDBStrategy)
        self.assertIsInstance(DatabaseStrategyFactory.get_strategy("redis"), RedisStrategy)

    def test_factory_invalid_type(self):
        with self.assertRaises(ValueError):
            DatabaseStrategyFactory.get_strategy("oracle")

    def test_mysql_connection_string(self):
        db = DatabaseConnection('mysql', 'localhost', 3306, 'user', 'pass', 'db', use_ssl=True)
        strategy = MySQLStrategy()
        conn_str = strategy.build_connection_string(db)
        self.assertIn("mysql://user:pass@localhost:3306/db", conn_str)
        self.assertIn("useSSL=true", conn_str)

    def test_postgresql_connection_string(self):
        db = DatabaseConnection('postgresql', 'pg.host', 5432, 'u', 'p', 'mydb', use_ssl=True)
        strategy = PostgreSQLStrategy()
        conn_str = strategy.build_connection_string(db)
        self.assertEqual(conn_str, "postgresql://u:p@pg.host:5432/mydb?sslmode=require")

    def test_mongodb_connection_string(self):
        db = DatabaseConnection('mongodb', 'mongo.host', 27017, 'admin', 'pass', 'analytics', pool_size=10, retry_attempts=5)
        strategy = MongoDBStrategy()
        conn_str = strategy.build_connection_string(db)
        self.assertIn("mongodb://admin:pass@mongo.host:27017/analytics", conn_str)
        self.assertIn("poolSize=10", conn_str)

    def test_redis_connection_string(self):
        db = DatabaseConnection('redis', 'redis.host', 6379, '', '', '0')
        strategy = RedisStrategy()
        conn_str = strategy.build_connection_string(db)
        self.assertEqual(conn_str, "redis.host:6379/0")

if __name__ == "__main__":
    unittest.main()
