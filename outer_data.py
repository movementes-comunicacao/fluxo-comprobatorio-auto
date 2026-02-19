from components.PlayWrightAuto_async.SocialMedia.Youtube import Youtube_Automation
from components.PlayWrightAuto_async.SocialMedia.TikTok import Tiktok_Automation
from components.PlayWrightAuto_async.SocialMedia.Threads import Threads_Automation
from components.PlayWrightAuto_async.SocialMedia.Twitter import Twitter_Automation
from components.PlayWrightAuto_async.essencial import PlayEssencial, logger
from components.Meta_Manager.module.meta_class import Social_Manager
from srcs.auto_sheets.social_extract import (
    get_face_essencial,
    get_insta_essencial,
    get_tiktok_essencial,
    get_youtube_essencial,
    get_threads_essencial,
    get_twitter_essencial
)
from srcs.utils import merge_posts
from utils.read_env import *
from srcs.auto_sheets.sheet_input import Date_Utils
import asyncio
import pandas as pd

async def run_sequence(dates, core):
    social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')

    ttk = Tiktok_Automation(TIKTOK_ACC, core)
    ytb = Youtube_Automation(YOUTUBE_ACC, core)
    th  = Threads_Automation(THREADS_ACC, core)
    twt = Twitter_Automation(TWITTER_ACC, core)

    tk_data  = await ttk.standard_procedure(dates) if TIKTOK_ACC else []
    yt_data  = await ytb.standard_procedure(dates) if YOUTUBE_ACC else []
    th_data  = await th.standard_procedure(dates)  if THREADS_ACC else []
    tw_data  = await twt.standard_procedure(dates) if TWITTER_ACC else []

    face_res  = get_face_essencial(social_man, dates)
    insta_res = get_insta_essencial(social_man, dates)
    tk_res = get_tiktok_essencial(tk_data)
    yt_res = get_youtube_essencial(yt_data)
    th_res = get_threads_essencial(th_data)
    tw_res = get_twitter_essencial(tw_data)

    result = merge_posts(
        face_res,
        insta_res,
        tk_res,
        yt_res,
        th_res,
        tw_res
    )

    return result

async def main():
    logger.info("Iniciando coleta...")

    dt = Date_Utils()
    period = dt.return_period()

    since = period["start_date"]["value"]
    until = period["final_date"]["value"]
    dates = [since, until]

    logger.info(f"Período → {since} até {until}")

  
    core = PlayEssencial(
        browser_data_path=BROWSER_DATA_PATH,
        chrome_executable_path=CHROME_EXECUTABLE_PATH
    )

    await core.start_browser_user()

    try:
        result = await run_sequence(dates, core)

        df = pd.DataFrame(result)
        print("GERANDO ARQUIVO EXCEL...",df)
        df.to_excel("Relatorio Geral Redes.xlsx", index=False)
        logger.info("Arquivo gerado com sucesso: Relatorio Geral Redes.xlsx")

        print("\n===== RESULTADO FINAL =====")
        print(result)

    finally:
        if core.page:
            await core.page.close()
        if core.browser:
            await core.browser.close()
        if core.playwright:
            await core.playwright.stop()



if __name__ == "__main__":
    asyncio.run(main())
