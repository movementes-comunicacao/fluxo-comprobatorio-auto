from main import env_variable_prefix
from components.cfg_manager.module.env_manager import Read_env

env_variables = Read_env('utils/' + env_variable_prefix + '.env').return_dict()