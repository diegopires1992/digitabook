from os import getenv


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_DEV")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL_UP_UP")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_DEV")
    testing=True


config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig,
}
