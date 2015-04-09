from server.AppStarter import AppStarter
import os

static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client")
app = AppStarter()
app.register_routes_to_resources(static_folder_root)
flask_runner = app.get_flask_runner()  # flask app instance for gunicorn


def runserver():
    app.run()

if __name__ == '__main__':
    runserver()

