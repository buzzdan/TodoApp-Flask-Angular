import os
from Server import AppStarter, EnvironmentSettingsLoader

root_folder_path = os.path.dirname(os.path.abspath(__file__))
static_folder_root = os.path.join(root_folder_path, "Client")

print('starting Server... ToDo is coming right at ya!')
# config_name = settings_loader['APP_SETTINGS']
# print('Setting up: '+config_name)

settings_loader = EnvironmentSettingsLoader(root_folder_path)

app = AppStarter(settings_loader)
app.register_routes_to_resources(static_folder_root)
flask_runner = app.get_flask_runner()  # flask app instance for gunicorn


def runserver():
    print('All set! Ruuuuuuuuunnnnning !')
    app.run()

if __name__ == '__main__':
    runserver()