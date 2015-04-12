import os

from server.AppStarter import AppStarter
from server.Utils.EnvironmentSettingsLoader import EnvironmentSettingsLoader


root_folder_path = os.path.dirname(os.path.abspath(__file__))
static_folder_root = os.path.join(root_folder_path, "client")

# Make this unique, and don't share it with anybody.
settings_loader = EnvironmentSettingsLoader(root_folder_path)
config_name = settings_loader['APP_SETTINGS']

print('starting server... ToDo is coming right at ya!')
print('Setting up: '+config_name)

app = AppStarter(settings_loader)
app.register_routes_to_resources(static_folder_root)
flask_runner = app.get_flask_runner()  # flask app instance for gunicorn


def runserver():
    print('All set! Ruuuuuuuuunnnnning !')
    app.run()

if __name__ == '__main__':
    runserver()