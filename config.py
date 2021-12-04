class Config(object):
    API_PORT = 9900
    # MONGO_URL = "mongodb+srv://1012hackathon:1012tkmce@cluster0.9tsp4.mongodb.net"
    MONGO_URL = "mongodb://localhost:27017/"


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class StagingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
