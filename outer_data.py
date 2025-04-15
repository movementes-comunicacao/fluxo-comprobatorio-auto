
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
	dates = dt_man.return_period()
	since = dates["start_date"]["value"]
	until = dates["final_date"]["value"]

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
		
		# Files_Handling("./data/").write_file(result, "data_result.json")
		# ytb.close_browser()