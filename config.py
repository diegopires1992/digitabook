from os import getenv


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JWT_SECRET_KEY = getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(Config):
    pass


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_DEV")
    testing=True


config_selector = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig,
}
