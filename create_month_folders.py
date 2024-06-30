from components.Driver_Flow.module.drive_auth_p import *
from utils.read_env import *
driver_m = Drive_Manager(CREDS_PATH + "token_pickle/token.pickle", CREDS_PATH + "oauth_cred.json")

folder_name=''
"""input the folder url which you will create the other folders inside"""

last_day = 31
for i in range(1, last_day+1):
        driver_m.create_drive_file("folder", folder_name, str(i))