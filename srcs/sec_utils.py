from components.Driver_Flow.module.drive_auth_p import *
from utils.read_env import *
from components.Sheets_Manager.module.sheets_manager import *
def create_month_folder(driver_m: Drive_Manager, month_fd_url:str):
	"""
	Create the folders of the days inside an specific url
	param: month_fd_url
	input the folder url which you will create the other folders inside
	"""

	last_day = 31
	for i in range(1, last_day+1):
		driver_m.create_drive_file("folder", month_fd_url, str(i))

# drive_m = Drive_Manager(CREDS_PATH + "token_pickle/token.pickle", CREDS_PATH + "oauth_cred.json")
# sheet_m = Sheets_Manager("https://docs.google.com/spreadsheets/d/19cG6ldny58xmZIAQ1uQmICMisy7m0gnpeUiC11L2jO0/", SERVICE_ACC, False)
print(env_variables)