import gspread
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager

def input_on_sheets(sh_man: Sheets_Manager):
        return(sh_man.get_line_response('config', 'Jun', column_search='E', column_response='G'))

