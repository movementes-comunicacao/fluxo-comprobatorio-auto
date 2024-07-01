
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from utils.read_env import *
from srcs.utils import *
from datetime import datetime
import pandas as pd

print(ACCOUNT, CONFIG_INI_PATH)


if __name__ == "__main__":
	sh_man = Sheets_Manager(SHEET_URL, SERVICE_ACC)
	social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
	twitter_man = Twitter_Manager(TWITTER_ACC, BROWSER_DATA_PATH, USER_AGENT, False)
	dt_man = Date_Utils()
	
	sh_config = sh_man.access_sheet('config')
	last_dt = datetime.strptime(sh_config.get("F15")[0][0], "%d/%m/%Y %H:%M:%S")
	# since = last_dt.replace(minute=last_dt.minute+10, second=0)
	since = datetime(2024, 6, 30)
	until = datetime.now().replace(day=30, month=6, hour=23, minute=59, second=59, microsecond=0)
	social_man.date_optional = [since, until]
	period = social_man.return_period()
	if since < until:
		print("nova solicitação!")
		# SeparateMonthsByReq precisa vir aqui -> para caso cada mês dê ruim.
		result = merge_posts(
			get_face_essencial(social_man, [since, until]),
			get_insta_essencial(social_man, [since, until]),
			get_twitter_essencial(twitter_man, [since, until])
			)
		pd.DataFrame(result).to_excel("Relatorio.xlsx")
		input_on_sheets(sh_man, result, period, dt_man)