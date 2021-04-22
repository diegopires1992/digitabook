from app import create_app

applications = create_app()
if __name__ == '__main__':
    applications.run("0.0.0.0")