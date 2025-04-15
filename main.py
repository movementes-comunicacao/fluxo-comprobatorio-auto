
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from components.Thread_Manager.module.scraping_threads import Threads_Manager
from datetime import datetime, timedelta
import pandas as pd
from components.Files_Handler.module.file_handler import Files_Handling
import sys

env_variable_prefix = "nit"
if __name__ == "__main__":
	social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
	ttk = None if TIKTOK_ACC == None else Tiktok_Automation(TIKTOK_ACC)
	ttk.start_browser()
	ytb = None if YOUTUBE_ACC == None else Youtube_Automation(YOUTUBE_ACC, ttk.browser, ttk.page)
	dateOpt = sys.argv
	print("DATE OPT LEN IS:", len(dateOpt))
	dt_man = Date_Utils()
	if SHEET_URL == "None" or len(dateOpt) > 1 and dateOpt[-1] == "dtchoose":
		dates = dt_man.return_period()
		since = dates["start_date"]["value"]
		until = dates["final_date"]["value"]
	else:
		sh_man = Sheets_Manager(SHEET_URL, SERVICE_ACC)
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
			getTwitterAndThreads([since, until]),
			get_insta_essencial(social_man, [since, until]),
			get_face_essencial(social_man, [since, until]),
			get_tiktok_essencial(ttk, [since, until]),
			get_youtube_essencial(ytb, [since, until]),
			)
		pd.DataFrame(result).to_excel("Relatorio.xlsx")
		if SHEET_URL != "None" and len(dateOpt) == 1:
			input_on_sheets(sh_man, result, period, dt_man)
		
		# Files_Handling("./data/").write_file(result, "data_result.json")
		# ytb.close_browser()