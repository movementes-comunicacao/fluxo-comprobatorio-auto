from components.cfg_manager.module.env_manager import Read_env

env_variables = Read_env('utils/.env').return_dict()

CONFIG_INI_PATH=env_variables["CONFIG_INI_PATH"]
ACCOUNT=env_variables["ACCOUNT"]
SHEET_URL=env_variables["SHEET_URL"]
SERVICE_ACC=env_variables['SERVICE_ACC_PATH']
USER_AGENT=env_variables['USER_AGENT']
BROWSER_DATA_PATH=env_variables['BROWSER_DATA_PATH']