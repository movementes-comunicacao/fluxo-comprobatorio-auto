from components.Meta_Manager.module.meta_class import Social_Manager
from utils.read_env import *

print(ACCOUNT, CONFIG_INI_PATH)
social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
