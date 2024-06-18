
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from utils.read_env import *
from srcs.utils import *
from datetime import datetime

print(ACCOUNT, CONFIG_INI_PATH)

sh_man = Sheets_Manager(SHEET_URL, SERVICE_ACC)
# social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
# twitter_man = Twitter_Manager('NiteroiPref', BROWSER_DATA_PATH, USER_AGENT)
if __name__ == "__main__":
	# sh_config = sh_man.access_sheet('config')
	# last_dt = datetime.strptime(sh_config.get("F15")[0][0], "%d/%m/%Y %H:%M:%S")
	# since = last_dt.replace(day=(last_dt.day)+1, hour=0, minute=0, second=0)
	# until = datetime.now().replace(day=datetime.now().day-1, hour=23, minute=59, second=59, microsecond=0)
	# if since < until:
	# 	print("nova solicitação!")
	# 	result = merge_posts(
	# 		get_face_essencial(social_man, [since, until]),
	# 		get_insta_essencial(social_man, [since, until]),
	# 		get_twitter_essencial(twitter_man, [since, until])
	# 		)
	print(input_on_sheets(sh_man))