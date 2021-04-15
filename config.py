from os import getenv


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DB_URI_DEV")
    JSON_SORT_KEYS = False


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
