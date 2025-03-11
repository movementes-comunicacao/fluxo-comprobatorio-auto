
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from components.Thread_Manager.module.scraping_threads import Threads_Manager
from datetime import datetime, timedelta
import pandas as pd

env_variable_prefix = "nit"
if __name__ == "__main__":

	sh_man = Sheets_Manager(SHEET_URL, SERVICE_ACC)
	social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
	# twitter_man = Twitter_Manager(TWITTER_ACC, BROWSER_DATA_PATH, USER_AGENT,"Default",other_options=False,disable_graphics=False, remote_connection=False)
	# threads_man = Threads_Manager("niteroipref", BROWSER_DATA_PATH, USER_AGENT,"Default",other_options=False,disable_graphics=False, remote_connection=False)
	dt_man = Date_Utils()
	sh_config = sh_man.access_sheet('config')
	last_dt = datetime.strptime(sh_config.get("F15")[0][0], "%d/%m/%Y %H:%M:%S")
	since = last_dt + timedelta(minutes=2)
	until = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(days=1)
	print("since is: ", since, "and until is: ", until)
	social_man.date_optional = [since, until]
	period = social_man.return_period()
	if since < until:
		print("nova solicitação!")
		# SeparateMonthsByReq precisa vir aqui -> para caso cada mês dê ruim.
		result = merge_posts(
			get_face_essencial(social_man, [since, until]),
			get_insta_essencial(social_man, [since, until]),
			getTwitterAndThreads([since, until])
			)
		# pd.DataFrame(result).to_excel("Relatorio.xlsx")
		input_on_sheets(sh_man, result, period, dt_man)