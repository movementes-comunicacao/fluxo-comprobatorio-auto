import asyncio
from datetime import datetime
from components.PlayWrightAuto_async.SocialMedia.Youtube import Youtube_Automation
from components.PlayWrightAuto_async.SocialMedia.TikTok import Tiktok_Automation
from components.PlayWrightAuto_async.SocialMedia.Threads import Threads_Automation
from components.PlayWrightAuto_async.SocialMedia.Twitter import Twitter_Automation
from components.Sheets_Manager.module.sheets_manager import Sheets_Manager
from components.Meta_Manager.module.meta_class import Social_Manager
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

async def main_youtube():
    yt = Youtube_Automation(
        account="PrefeituradeNiteróiOficial",
        browser_data_path="C:/profile_youtube",
        chrome_executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
    )
    return await yt.standard_procedure([
        datetime(2025, 12, 1),
        datetime(2025, 12, 3)
    ])

async def main_tiktok():
    tik = Tiktok_Automation(
        account="niteroipref",
        browser_data_path="C:/profile_tiktok",
        chrome_executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
    )
    return await tik.standard_procedure([
        datetime(2025, 12, 1),
        datetime(2025, 12, 3)
    ])

async def main_thread():
    th = Threads_Automation(
        account="niteroipref",
        browser_data_path="C:/profilex",
        chrome_executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
    )
    return await th.standard_procedure([
        datetime(2025, 12, 1),
        datetime(2025, 12, 3)
    ])

async def twitter_main():
    tw = Twitter_Automation(
        account="niteroipref",
        browser_data_path="C:/profile_twitter",
        chrome_executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe"
    )
    return await tw.standard_procedure([
        datetime(2025, 12, 1),
        datetime(2025, 12, 3)
    ])

async def run_parallel():
    yt_res, tk_res, th_res, tw_res = await asyncio.gather(
        main_youtube(),
        main_tiktok(),
        main_thread(),
        twitter_main(),
        return_exceptions=True
    )
    get_face_essencial
    outputs = [yt_res, tk_res, th_res, tw_res]
              
               

    print("\n======= RESULTADOS =======")
    for r in outputs:
        print(r)

asyncio.run(run_parallel())
