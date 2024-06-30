from components.cfg_manager.module.env_manager import Read_env

env_prefix = 'marica'
"""the name of the .env file before the '.'.
For now we have 2 possible values: marica and nit"""
env_variables = Read_env('utils/' + env_prefix + '.env').return_dict()

CONFIG_INI_PATH=env_variables["CONFIG_INI_PATH"]
ACCOUNT=env_variables["ACCOUNT"]
SHEET_URL=env_variables["SHEET_URL"]
SERVICE_ACC=env_variables['SERVICE_ACC_PATH']
USER_AGENT=env_variables['USER_AGENT']
BROWSER_DATA_PATH=env_variables['BROWSER_DATA_PATH']
CREDS_PATH=env_variables["CREDS_PATH"]
TWITTER_ACC=env_variables["TWITTER_ACC"]