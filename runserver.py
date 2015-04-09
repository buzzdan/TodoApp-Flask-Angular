from server.AppStarter import AppStarter
import os

print('starting server... ToDo is coming right at ya!')

static_folder_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "client")
app = AppStarter()
app.register_routes_to_resources(static_folder_root)
flask_runner = app.get_flask_runner()  # flask app instance for gunicorn

def runserver():
    app.run()

if __name__ == '__main__':
    runserver()

    # I should learn how to use those local environment variables...
    # Heroku uses the settings from the .env file and i should define it someway in pycharm ide...
    # secret_key = str(os.environ.get('APP_SETTINGS'))
    # print('starting environment variables! - app settings are:' + secret_key)

