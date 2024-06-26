from gspread.worksheet import Worksheet
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from datetime import datetime
from components.Date_Utils.module.date_time_utils import Date_Utils

def arr_sep_by_month(metrics: list[dict], req_arr: dict[list])->None:
	"""get the post by post json, format the date string to datetime format and append on the 
	specific requisitions on a array with the key of the number of the related month."""
	for post in metrics:
		date = datetime.strptime(post['date_created'][0:10], "%Y-%m-%d")
		# Essa linha transforma uma string de data num elemento datetime.
		# post['date_created'] = date
		month = date.month
		req_arr.get(month).append(post)

def separate_months_req(metrics: list[dict], months: dict):
	since_prop = months['start_date']
	until_prop = months['final_date']
	period_range = until_prop['num_mes'] - since_prop['num_mes'] + 1
	result_arr = {since_prop.get('num_mes') + i: [] for i in range (0, period_range)}
	arr_sep_by_month(metrics, result_arr)
	return result_arr

def access_or_create_sheet(sh_man: Sheets_Manager, sheet_name=None) -> Worksheet | None:
	list_sheets = [i.title for i in  sh_man.spreadsheet_obj.worksheets()]
	if sheet_name in list_sheets:
		return sh_man.access_sheet(sheet_name)
	else:
		print(f"Guia {sheet_name} não localizada, necessita de um processo individual de criação.")
		return None


def input_on_sheets(sh_man: Sheets_Manager, metrics: list[dict], months:dict, date_man: Date_Utils):
	result_arr = separate_months_req(metrics, months)
	del metrics
	for month_num, arr in result_arr.items():
		sheet_name = date_man.months["portuguese"].get(month_num).capitalize()[0:3]
		print("sheet name é ", sheet_name)
		sheet_obj = access_or_create_sheet(sh_man, sheet_name)
		if sheet_obj == None:
			continue
		last_line = float(sh_man.get_line_response("config", str(month_num), "D", "G").replace(",","."))
		sh_man.input_data(arr, sheet_obj, 'C'+str(int(last_line) + 1),["description"])
		sh_man.input_data(arr, sheet_obj, 'E'+str(int(last_line) + 1),["link_url"])
		sh_man.input_data(arr, sheet_obj, 'I'+str(int(last_line) + 1),["date_created"])