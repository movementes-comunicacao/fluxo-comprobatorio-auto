from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from utils.read_env import *
def get_last_date_from_sheets(sheets: Sheets_Manager, cfg_sheet):
        pass

if __name__ == "__main__":
        sh_man = Sheets_Manager(SHEET_URL, SERVICE_ACC)
        sh_man.access_sheet('config')
        