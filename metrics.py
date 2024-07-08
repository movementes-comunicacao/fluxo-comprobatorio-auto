from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from srcs.auto_sheets.social_extract import *
from srcs.auto_sheets.sheet_input import *
from utils.read_env import *
from srcs.utils import *
from datetime import datetime
import pandas as pd

def get_pd_metrics(twitter_man: Twitter_Manager, since, until):
	if since < until:
		print("nova solicitação!")
		result = get_twitter_essencial(twitter_man, [since, until])
		normalized = pd.json_normalize(result)
		normalized.to_excel("relatorio.xlsx")

def get_face_metrics(social_man: Social_Manager, since, until):
	if since < until:
		result = get_face_essencial(social_man, [since, until])
		return result