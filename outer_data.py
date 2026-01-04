
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from components.Thread_Manager.module.scraping_threads import Threads_Manager
from datetime import datetime, timedelta
import pandas as pd
from components.Files_Handler.module.file_handler import Files_Handling
import sys
from srcs.utils import merge_posts
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

env_variable_prefix = "nit"
if __name__ == "__main__":
	social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')
	
	ttk = None if TIKTOK_ACC == None else TikTok.Tiktok_Automation(TIKTOK_ACC)
	ttk.start_browser()
	ytb = None if YOUTUBE_ACC == None else Youtube.Youtube_Automation(YOUTUBE_ACC, ttk.playwright, browser=ttk.browser, page=ttk.page)
	twt = None if TWITTER_ACC == None else Twitter.Twitter_Automation(TWITTER_ACC, ttk.playwright, browser_data_path=BROWSER_DATA_PATH, chrome_executable_path=CHROME_EXECUTABLE_PATH)
	threads = None if THREADS_ACC == None else Threads.Threads_Automation(THREADS_ACC, ttk.playwright, browser_data_path=BROWSER_DATA_PATH, chrome_executable_path=CHROME_EXECUTABLE_PATH)

	dateOpt = sys.argv
	logger.info(f"DATE OPT LEN IS: {len(dateOpt)}")
	dt_man = Date_Utils()
	dates = dt_man.return_period()
	since = dates["start_date"]["value"]
	until = dates["final_date"]["value"]

	logger.info(f"since is: {since} and until is: {until}")
	social_man.date_optional = [since, until]
	period = social_man.return_period()
	if since < until:
		logger.info("nova solicitação!")
		# SeparateMonthsByReq precisa vir aqui -> para caso cada mês dê ruim.
		result = merge_posts(
			# get_tiktok_essencial(ttk, [since, until]),
			# get_twitter_essencial(twt, [since, until]),
			get_threads_essencial(threads, [since, until]),
			# get_insta_essencial(social_man, [since, until]),
			# get_face_essencial(social_man, [since, until]),
			# get_youtube_essencial(ytb, [since, until]),
			)
		try:
			pd.DataFrame(result).to_excel("Relatorio metricas.xlsx")
		except Exception as e:
			logger.error(f"Error writing to Excel: {e}")

		
		# Files_Handling("./data/").write_file(result, "data_result.json")
		# ytb.close_browser()