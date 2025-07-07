from utils.defining_env import env_variables

CONFIG_INI_PATH=env_variables["CONFIG_INI_PATH"]
ACCOUNT=env_variables["ACCOUNT"]
SERVICE_ACC=env_variables['SERVICE_ACC_PATH']
USER_AGENT=env_variables['USER_AGENT']
BROWSER_DATA_PATH=env_variables['BROWSER_DATA_PATH']
CHROME_EXECUTABLE_PATH=env_variables['CHROME_EXECUTABLE_PATH']
CREDS_PATH=env_variables["CREDS_PATH"]
SHEET_URL=env_variables.get("SHEET_URL")
TWITTER_ACC=env_variables.get("TWITTER_ACC")
THREADS_ACC = env_variables.get("THREADS_ACC")
YOUTUBE_ACC = env_variables.get("YOUTUBE_ACC")
TIKTOK_ACC = env_variables.get("TIKTOK_ACC")


# Locators for Threads
column_body_locator = '//div[@aria-label="Corpo da coluna"]'
feed_container = '//div[@class="x1a2a7pz x1n2onr6"]'
post_items = '//div[@class="xrvj5dj xd0jker x1evr45z"]'
post_date_link = '//div[@class="x78zum5 x1c4vz4f x2lah0s"]//a[@class="x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1lku1pv x12rw4y6 xrkepyr x1citr7e x37wo2f"]'