import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = os.getenv("PORT", ":5000")
    SERVER_NAME = f"{HOST}{PORT}"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super secret")


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
