from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from components.Thread_Manager.module.scraping_threads import Threads_Manager
from components.Meta_Manager.module.meta_class import Social_Manager
from components.PlayWrightAuto.SocialMedia.TikTok import Tiktok_Automation
from components.Twitter_Manager.module.scraping_twt import Twitter_Manager, BeautifulSoup
from components.PlayWrightAuto.SocialMedia import TikTok, Threads, Twitter, Youtube
# from components.PlayWrightAuto.SocialMedia.Twitter import Twitter_Automation
from utils.read_env import *

def get_face_essencial(social_man: Social_Manager, dates: list)->list:        
	result =[]
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

def get_tiktok_essencial(dates: list)->list:
	tiktok_man = TikTok.Tiktok_Automation(ACCOUNT)
	model = tiktok_man.standard_procedure(dates)
	result = []
	for feed in model:
		for link, post in feed.items():
			result.append(
				{
				'description': post['desc'],
				'views': post['views'],
				'link': link,
				}
			)
	return result

def get_threads(dates: list)->list:
	threads_man = Threads.Threads_Automation(ACCOUNT)
	model = threads_man.standard_procedure(dates)
	result = []
	for feed in model:
		for link, post in feed.items():
			result.append(
				{
				'date_created': post['Data'],
				'description': post['Descrição'],
				'link': link,
				}
			)
	return result

def get_twitter_essencial(dates: list)->list:
	twitter_man = Twitter.Twitter_Automation(ACCOUNT)
	model = twitter_man.standard_procedure(dates)
	result = []
	for feed in model:
		for link, post in feed.items():
			result.append(
				{
				'date_created': post['Data'],
				'description': post['Descrição'],
				'link': link,
				}
			)
	return result

def get_youtube_essencial(dates: list)->list:
	youtube_man = Youtube.Youtube_Automation(ACCOUNT)
	model = youtube_man.standard_procedure(dates)
	result = []
	for feed in model:
		for link, post in feed.items():
			result.append(
				{
				'date_created': post['date'],
				'title': post['title'],
				'link': link,
				}
			)
	return result


def getTwitterAndThreads(dates: list)->list:
	result = []
	if (TWITTER_ACC != None):
		twitter_man = Twitter_Manager(TWITTER_ACC, BROWSER_DATA_PATH, USER_AGENT,"Default",other_options=False,disable_graphics=False, remote_connection=False)
		model = twitter_man.standard_procedure(dates)
		for post in model:
			result.append(
				{
				'date_created': post['extra_1'],
				'metrics': post['extra_2'],
				'description': post['texts'],
				'link_url': post['effective_link']
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
	
def get_threads_essencial(threads_man: Threads_Manager | None, dates: list)->list:
	result = []
	if threads_man != None:
		model = threads_man.standard_procedure(dates)
		for post in model:
			result.append(
				{
				'date_created': post['extra_1'],
				'description': post['texts'],
				'link_url': post['effective_link']
				}
			)
	return result

def get_youtube_essencial(youtb: Youtube_Automation | None, dates:list):
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