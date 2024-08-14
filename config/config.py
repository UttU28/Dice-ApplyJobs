# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_CONFIG = {
    'server': os.getenv('DB_SERVER'),
    'database': os.getenv('DB_DATABASE'),
    'username': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
}

CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH')
CHROME_OPTIONS = {
    'debugger_address': os.getenv('CHROME_DEBUGGER_ADDRESS')
}

AZURE_BLOB_CONFIG = {
    'account_name': os.getenv('AZURE_ACCOUNT_NAME'),
    'account_key': os.getenv('AZURE_ACCOUNT_KEY'),
    'container_name': os.getenv('AZURE_CONTAINER_NAME'),
}
