import yaml

SETTINGS_FILEPATH = '../tests/settings/default.yaml'

def read_settings_file():
    with open(SETTINGS_FILEPATH) as file:
        TEST_ATTR = yaml.load(file, Loader=yaml.FullLoader)
    return TEST_ATTR