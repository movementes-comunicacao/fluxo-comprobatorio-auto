
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from components.Thread_Manager.module.scraping_threads import Threads_Manager
from datetime import datetime, timedelta
import pandas as pd
from components.Files_Handler.module.file_handler import Files_Handling
import sys
from srcs.utils import merge_posts

env_variable_prefix = "nit"
if __name__ == "__main__":
	social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
	
	ttk = None if TIKTOK_ACC == None else TikTok.Tiktok_Automation(TIKTOK_ACC)
	ttk.start_browser()
	ytb = None if YOUTUBE_ACC == None else Youtube.Youtube_Automation(YOUTUBE_ACC, ttk.playwright, browser=ttk.browser, page=ttk.page)
	twt = None if TWITTER_ACC == None else Twitter.Twitter_Automation(TWITTER_ACC, ttk.playwright, browser_data_path=BROWSER_DATA_PATH, chrome_executable_path=CHROME_EXECUTABLE_PATH)
	threads = None if THREADS_ACC == None else Threads.Threads_Automation(THREADS_ACC, ttk.playwright, browser=twt.browser,browser_data_path=BROWSER_DATA_PATH, chrome_executable_path=CHROME_EXECUTABLE_PATH)

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
			get_insta_essencial(social_man, [since, until]),
			get_face_essencial(social_man, [since, until]),
			get_twitter_essencial(twt, [since, until]),
			get_threads_essencial(threads, [since, until]),
			get_youtube_essencial(ytb, [since, until]),
			get_tiktok_essencial(ttk, [since, until]),
			)
		try:
			pd.DataFrame(result).to_excel("Relatorio.xlsx")
		except Exception as e:
			print("Error writing to Excel:", e)
		if SHEET_URL != "None" and len(dateOpt) == 1:
			input_on_sheets(sh_man, result, period, dt_man)
		
		# Files_Handling("./data/").write_file(result, "data_result.json")
		# ytb.close_browser()