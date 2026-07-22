import asyncio
from datetime import datetime
from pathlib import Path
import pandas as pd
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

# Caminho do arquivo JSON da sessão salva
STORAGE_STATE_PATH = Path("./state.json")


async def setup_login():
    """Realiza o login inicial manualmente e salva a sessão no state.json."""
    print("\n--- CONFIGURAÇÃO DE LOGIN INICIAL ---")
    bot = PlayEssencial(storage_state_path=str(STORAGE_STATE_PATH))
    await bot.start_browser()

    # Abre a página de login do Google
    await bot.page.goto("https://accounts.google.com/")

    input("👉 Faça o login manualmente no navegador que abriu e pressione ENTER no terminal...")

    # Salva os cookies e storage no arquivo JSON
    await bot.save_storage_state()
    await bot.stop_browser()
    print("✅ Sessão salva com sucesso! Continuando fluxo de automação...\n")


async def _run_platform(name: str, factory, account, dates):
    """
    Executa a coleta de uma única rede social de forma isolada.
    """
    if not account:
        logger.info(f"[{name}] conta não configurada; pulando.")
        return None

    try:
        automation = factory(account)
        return await automation.standard_procedure(dates)
    except Exception as exc:
        logger.error(f"[{name}] falha durante a coleta: {exc}", exc_info=True)
        return None


async def run_sequence(dates, core):
    social_man = Social_Manager(ACCOUNT, CONFIG_INI_PATH, './data')

    tk_data = await _run_platform("TikTok", lambda acc: Tiktok_Automation(acc, core), TIKTOK_ACC, dates)
    # yt_data = await _run_platform("YouTube", lambda acc: Youtube_Automation(acc, core), YOUTUBE_ACC, dates)
    # th_data = await _run_platform("Threads", lambda acc: Threads_Automation(acc, core), THREADS_ACC, dates)
    # tw_data = await _run_platform("Twitter", lambda acc: Twitter_Automation(acc, core), TWITTER_ACC, dates)

    tk_res = get_tiktok_essencial(tk_data) if tk_data is not None else None

    try:
        result = merge_posts(
            tk_res,
        )
    except Exception as exc:
        logger.error(f"Falha ao mesclar resultados das redes: {exc}", exc_info=True)
        raise

    return result


async def main():
    logger.info("Iniciando coleta...")

    # Se o arquivo state.json não existir na pasta, solicita o login primeiro
    if not STORAGE_STATE_PATH.exists():
        await setup_login()

    dt = Date_Utils()
    period = dt.return_period()

    since = period["start_date"]["value"]
    until = period["final_date"]["value"]
    dates = [since, until]

    logger.info(f"Período → {since} até {until}")

    # Inicializa o core passando o caminho do estado salvo
    core = PlayEssencial(
        storage_state_path=str(STORAGE_STATE_PATH),
        browser_data_path=BROWSER_DATA_PATH,
        chrome_executable_path=CHROME_EXECUTABLE_PATH
    )

    # Inicia o navegador reutilizando a sessão do state.json
    await core.start_browser()

    try:
        result = await run_sequence(dates, core)

        df = pd.DataFrame(result)

        output_dir = Path("./reports")
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_path = output_dir / f"Relatorio Geral Redes {timestamp}.xlsx"

        print("GERANDO ARQUIVO EXCEL...")
        try:
            df.to_excel(output_path, index=False)
            logger.info(f"Arquivo gerado com sucesso: {output_path}")
        except PermissionError:
            logger.error(
                f"Não foi possível salvar '{output_path}' — verifique se o "
                "arquivo não está aberto em outro programa."
            )
        except Exception as exc:
            logger.error(f"Falha inesperada ao salvar o Excel: {exc}", exc_info=True)

        print("\n===== RESULTADO FINAL =====")
        print(result)

    finally:
        # Encerra o navegador e a instância do Playwright de forma limpa
        await core.stop_browser()


if __name__ == "__main__":
    asyncio.run(main())