"""
This file stores all the possible configurations for the Flask app.
Changing configurations like the secret key or the database
url should be stored as environment variables and imported
using the 'os' library in Python.
"""
import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SSL = os.getenv('POSTGRESQL_SSL', True)
    if isinstance(SSL, str):
        SSL = SSL.lower() in ['true', '1', 'yes', "t"]
    DATABASE = os.getenv('POSTGRESQL_DATABASE', 'postgres')
    HOST = os.getenv('POSTGRESQL_HOST', 'localhost')
    PORT = os.getenv('POSTGRESQL_PORT', 5432 )
    USERNAME = os.getenv('POSTGRESQL_USERNAME', 'root')
    PASSWORD = os.getenv('POSTGRESQL_PASSWORD', 'YourStrong!Passw0rd')
    COLLECT_METRICS_INTERVAL_SEC = int(
        os.getenv('COLLECT_METRICS_INTERVAL_SEC', 120))
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
