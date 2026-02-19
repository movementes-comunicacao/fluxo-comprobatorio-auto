from datetime import datetime
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

def get_tiktok_essencial(data) -> list:
    if data is None:
        return []
    result = []
    print("DATA TIKTOK IS: ", data)
    input("PAUSA")
    for item in data:
        for link, info in item.items():
            result.append(
                {
                'date_created': info.get('date_created', ''),
                'description': info.get('description', ''),
                'link_url': link,
                'views': info.get('views', 0),
                'likes': info.get('likes', 0),
                'comments': info.get('comments', 0),
                'shares': info.get('shares', 0),
                'reposts': info.get('reposts', 0),
                'save': info.get('save', 0),
                
                }
            )
    return result

def get_youtube_essencial(data) -> list:
    if data is None:
        return []
    result = []
    print("DATA YOUTUBE IS: ", data)
    input("PAUSA")
    for item in data:
        for link, info in item.items():
            dt = info.get('date_create', '')
            formatted = dt.strftime("%d/%m/%Y %H:%M:%S")
            result.append(
                {
                'date_created': formatted,
                'description': info.get('description', ''),
                'link_url': link,
                'views': info.get('views', 0),
                'likes': info.get('likes', 0),
                'comments': info.get('comments', 0),
                }
            )
    return result

def get_threads_essencial(data) -> list:
    if data is None:
        return []
    result = []
    print("DATA THREADS IS: ", data)
    input("PAUSA")
    for item in data:
        result.append(
            {
            'date_created': item.get('date_created', ''),
            'description': item.get('description', ''),
            'link_url': item.get('link_url', ''),
            'visualizations': item.get('visualizations', 0),
            'likes': item.get('likes', 0),
            'comments': item.get('comments', 0),
            'shares': item.get('shares', 0),
            'reposts': item.get('reposts', 0),
            }
        )
    return result

def get_twitter_essencial(data) -> list:
    if data is None:
        return []
    result = []
    print("DATA TWITTER IS: ", data)
    input("PAUSA")
    for item in data:
        for link, info in item.items():
            result.append(
                {
                'date_created': info.get('date_created', ''),
                'description': info.get('description', ''),
                'link_url': link,
                'views': info.get('views', 0),
                'likes': info.get('likes', 0),
                'comments': info.get('comments', 0),
                'shares': info.get('shares', 0),
                }
            )
    return result