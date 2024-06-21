import gspread
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from datetime import datetime

def input_on_sheets(sh_man: Sheets_Manager, metrics: list[dict], months:dict):
	since_prop = months['start_date']
	until_prop = months['final_date']
	since_month = str(since_prop.get('mes')).capitalize()[0:3]
	until_month = str(until_prop.get('mes')).capitalize()[0:3]
	if since_month == until_month:
		print("é igual")
	else:
		
		separate_months_req(sh_man, metrics, months)
	return 'terminei'
	# return(sh_man.get_line_response('config', until_month, column_search='E', column_response='G'))
	

def arr_sep_by_month(metrics: list[dict], req_arr: dict[list])->None:
	for post in metrics:
		date = datetime.strptime(post['date_created'][0:10], "%Y-%m-%d")
		# Essa linha transforma uma string de data num elemento datetime.
		post['date_created'] = date
		month = date.month
		req_arr.get(month).append(post)

def separate_months_req(metrics: list[dict], months: dict):
	since_prop = months['start_date']
	until_prop = months['final_date']
	period_range = until_prop['num_mes'] - since_prop['num_mes'] + 1
	result_arr = {since_prop.get('num_mes') + i: [] for i in range (0, period_range)}
	arr_sep_by_month(metrics, result_arr)
	return result_arr
