from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from components.Meta_Manager.module.meta_class import Social_Manager
from components.PlayWrightAuto_async.SocialMedia import TikTok, Youtube, Threads, Twitter
from utils.read_env import *

def get_face_essencial(social_man: Social_Manager, dates: list) -> list:
    result = []
    if social_man is not None:
        model = social_man.face_description(dates)
        for post in model[0]:
            result.append({
                'date_created': post['created_time'],
                'description': post['message'],
                'link_url': post['permalink_url']
            })
    return result


def get_insta_essencial(social_man: Social_Manager, dates: list) -> list:
    result = []
    if social_man is not None:
        model = social_man.insta_description(dates)
        for post in model[0]:
            result.append({
                'date_created': post['timestamp'],
                'description': post.get('caption'),
                'link_url': post['permalink']
            })
    return result


