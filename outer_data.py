import asyncio
from datetime import datetime
import pandas as pd
import logging
import sys
from components.PlayWrightAuto_async.SocialMedia.Youtube import Youtube_Automation
from components.PlayWrightAuto_async.SocialMedia.TikTok import Tiktok_Automation
from components.PlayWrightAuto_async.SocialMedia.Threads import Threads_Automation
from components.PlayWrightAuto_async.SocialMedia.Twitter import Twitter_Automation
from components.PlayWrightAuto_async.essencial import logger
from components.Meta_Manager.module.meta_class import Social_Manager
from srcs.auto_sheets.social_extract import (
    get_face_essencial,
    get_insta_essencial,
)
from srcs.utils import merge_posts
from utils.read_env import *
from srcs.auto_sheets.sheet_input import Date_Utils



async def run_youtube(dates):
    if YOUTUBE_ACC is None:
        return []
    try:
        yt = Youtube_Automation(
            account=YOUTUBE_ACC,
            browser_data_path="C:/profile_youtube",
            chrome_executable_path=CHROME_EXECUTABLE_PATH,
        )
        return await yt.standard_procedure(dates)
    except Exception as e:
        logger.error(f"Erro YouTube: {e}")
        return []


async def run_tiktok(dates):
    if TIKTOK_ACC is None:
        return []
    try:
        tk = Tiktok_Automation(
            account=TIKTOK_ACC,
            browser_data_path="C:/profile_tiktok",
            chrome_executable_path=CHROME_EXECUTABLE_PATH,
        )
        return await tk.standard_procedure(dates)
    except Exception as e:
        logger.error(f"Erro TikTok: {e}")
        return []


async def run_threads(dates):
    if THREADS_ACC is None:
        return []
    try:
        th = Threads_Automation(
            account=THREADS_ACC,
            browser_data_path="C:/profilex",
            chrome_executable_path=CHROME_EXECUTABLE_PATH,
        )
        return await th.standard_procedure(dates)
    except Exception as e:
        logger.error(f"Erro Threads: {e}")
        return []


async def run_twitter(dates):
    if TWITTER_ACC is None:
        return []
    try:
        tw = Twitter_Automation(
            account=TWITTER_ACC,
            browser_data_path="C:/profile_twitter",
            chrome_executable_path=CHROME_EXECUTABLE_PATH,
        )
        return await tw.standard_procedure(dates)
    except Exception as e:
        logger.error(f"Erro Twitter: {e}")
        return []



async def run_parallel(dates, social_man):

   
    yt_res, tk_res, th_res, tw_res = await asyncio.gather(
        run_youtube(dates),
        run_tiktok(dates),
        run_threads(dates),
        run_twitter(dates),
    )

    # Redes Meta (não async)
    face_res = get_face_essencial(social_man, dates)
    insta_res = get_insta_essencial(social_man, dates)

   
    result = merge_posts(
        yt_res,
        tk_res,
        th_res,
        tw_res,
        face_res,
        insta_res,
    )

    return result



async def main():

    logger.info("Iniciando coleta...")

    dt = Date_Utils()
    period = dt.return_period()

    since = period["start_date"]["value"]
    until = period["final_date"]["value"]

    dates = [since, until]

    logger.info(f"Período → {since}  até  {until}")

   
    social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, "./data")
    social_man.date_optional = dates

 
    result = await run_parallel(dates, social_man)

 
    try:
        df = pd.DataFrame(result)
        df.to_excel("Relatorio Geral Redes.xlsx", index=False)
        logger.info("Arquivo gerado com sucesso: Relatorio Geral Redes.xlsx")
    except Exception as e:
        logger.error(f"Erro ao salvar Excel: {e}")

    print("\n===== RESULTADO FINAL =====")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
