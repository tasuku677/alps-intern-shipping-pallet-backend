import os
from typing import Callable
import sys


DEFAULT_CONFIG = {
    'API_URL': '/',
    'DATABASE_SERVER': 'sql04.cz.alps.eu',
    'DATABASE_USERNAME': 'WHappsApplicationUser',
    'DATABASE_PASSWORD': 'whapps',
    'DATABASE_NAME': 'WHapps',
    'TABLE_NAME': 'SQL04.WHapps.export.ShipmentPalletVisualCheck',
    'FOLDER_SEPARATOR': r'(\d{4})-(\d{2})-(\d{2})',
    'SERVER_PORT': 8000
}

def get_config(name: str, default=None, wrapper: Callable = None):
    if not wrapper:
        wrapper = lambda x: x   
    return wrapper(os.getenv(name, DEFAULT_CONFIG.get(name, default)))


def get_command_line_args():
    for _, args in  enumerate(sys.argv[1:]):
        print(args)
        

# Example usage:
# command_line_args = get_command_line_args()

# DEFAULT_CONFIG=yaml.load(pkg_resources.resource_stream('tasuku_app', 'config.yaml'), Loader=yaml.FullLoader)

#
# FOLDER_SEPARATOR="YYYYMMDD"
# PORT = 8000
#Process
# 1. Read the default configuration file (for example, default config.yaml)
# 2. Read the user configuration file. 
# 3. Read the environment variables

# tasuku_app

# $ tasuku_app --config-file my_config.yaml

# $set TASUKU_APP_DATABASE_PASSWORD=whapps
# $ tasuku_app
# ]
