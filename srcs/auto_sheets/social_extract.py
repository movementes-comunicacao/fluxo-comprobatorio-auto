from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from components.Thread_Manager.module.scraping_threads import Threads_Manager
from components.Meta_Manager.module.meta_class import Social_Manager
from components.Twitter_Manager.module.scraping_twt import Twitter_Manager, BeautifulSoup
from components.PlayWrightAuto.SocialMedia import TikTok, Threads, Twitter, Youtube
# from components.PlayWrightAuto.SocialMedia.Twitter import Twitter_Automation
from utils.read_env import *

def get_face_essencial(social_man: Social_Manager, dates: list)->list:        
	result =[]
	if social_man != None:
		model = social_man.face_description(dates)
		for post in model[0]:
			result.append(
				{
				'date_created': post['created_time'],
				'description': post['message'],
				'link_url': post['permalink_url']
				}
			)
	return result

def get_insta_essencial(social_man: Social_Manager, dates: list)->list:
	result =[]
	if social_man != None:
		model = social_man.insta_description(dates)
		for post in model[0]:
			result.append(
				{
				'date_created': post['timestamp'],
				'description': post.get('caption'),
				'link_url': post['permalink']
				}
			)
	return result

def get_tiktok_essencial(tiktok_man: TikTok.Tiktok_Automation, dates: list)->list:
	result = []
	if tiktok_man != None:
		models = tiktok_man.standard_procedure(dates)
		for link, post in models.items():
			result.append(
				{
				"date_created": post['date_created'],
				'description': post['description'],
				'link_url': link,
				'views': post['views'],
				}
			)
	return result

def get_threads_essencial(threads_man: Threads.Threads_Automation, dates: list)->list:
	result = []
	if threads_man != None:
		model = threads_man.standard_procedure(dates)
		for link, post in model.items():
			result.append(
				{
				'date_created': post['Data'],
				'description': post['Descrição'],
				'link_url': link,
				}
			)
	return result

def get_twitter_essencial(twitter_man : Twitter.Twitter_Automation, dates: list)->list:
	result = []
	if twitter_man != None:
		model = twitter_man.standard_procedure(dates)
		for link, post in model.items():
			result.append(
				{
				'date_created': post['Data'],
				'description': post['Descrição'],
				'link_url': link,
				}
			)
	return result


def get_youtube_essencial(youtb: Youtube.Youtube_Automation | None, dates:list):
	result = []
	if youtb != None:
		model = youtb.standard_procedure(dates)
		for link, data in model.items():
			result.append(
				{
				'date_created': data["date"],
				'description': data["title"],
				'link_url': link
				}
			)
	return result

# DEPRECATED
def getTwitterAndThreads(dates: list)->list:
	result = []
	if (TWITTER_ACC != None):
		twitter_man = Twitter_Manager(TWITTER_ACC, BROWSER_DATA_PATH, USER_AGENT,"Default",other_options=False,disable_graphics=False, remote_connection=False)
		model = twitter_man.standard_procedure(dates)
		for post in model:
			result.append(
				{
				'date_created': post['extra_1'],
				'description': post['texts'],
				'link_url': post['effective_link'],
				'metrics': post['extra_2'],
				}
			)
		twitter_man.driver.quit()
	if (THREADS_ACC != None):
		threads_man = Threads_Manager(THREADS_ACC, BROWSER_DATA_PATH, USER_AGENT,"Default",other_options=False,disable_graphics=False, remote_connection=False)
		model = threads_man.standard_procedure(dates)
		for post in model:
			result.append(
				{
				'date_created': post['extra_1'],
				'description': post['texts'],
				'link_url': post['effective_link']
				}
			)
		threads_man.driver.quit()
	return result