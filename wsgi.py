from app import create_app

application = create_app("production")
if __name__ == '__main__':
    application.run("0.0.0.0")