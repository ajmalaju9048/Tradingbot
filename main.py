"""
Main entry point.
Runs the Telegram bot + FastAPI server concurrently.
"""
import asyncio
import logging
import signal
import sys

import uvicorn
from telegram.ext import Application

from config import config
from db.database import init_db
from bot.handlers import build_application
from bot.notifications import BackgroundScheduler
from api.server import app as fastapi_app

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


async def run_fastapi():
    """Run FastAPI with uvicorn."""
    server_config = uvicorn.Config(
        fastapi_app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level=config.LOG_LEVEL.lower(),
        access_log=False,
    )
    server = uvicorn.Server(server_config)
    await server.serve()


async def run_telegram_bot(scheduler: BackgroundScheduler):
    """Run the Telegram bot (polling mode)."""
    tg_app = build_application()

    await tg_app.initialize()
    await tg_app.start()

    # Start background scheduler
    await scheduler.start()

    logger.info("Telegram bot started (polling).")
    await tg_app.updater.start_polling(drop_pending_updates=True)

    # Keep running until cancelled
    stop_event = asyncio.Event()

    def _signal_handler():
        stop_event.set()

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _signal_handler)

    await stop_event.wait()

    # Graceful shutdown
    await scheduler.stop()
    await tg_app.updater.stop()
    await tg_app.stop()
    await tg_app.shutdown()
    logger.info("Telegram bot stopped.")


async def main():
    logger.info("=" * 52)
    logger.info("  AI Trading Bot — Starting up")
    logger.info(f"  AI Provider : Google Gemini (3-tier)")
    logger.info(f"  Lite model  : {config.GEMINI_LITE_MODEL}")
    logger.info(f"  Flash model : {config.GEMINI_FLASH_MODEL}")
    logger.info(f"  Pro model   : {config.GEMINI_PRO_MODEL}")
    logger.info(f"  Daily limit : {config.GEMINI_DAILY_CALL_LIMIT} calls")
    logger.info(f"  Strategy    : {config.DEFAULT_STRATEGY}")
    logger.info(f"  Environment : {config.ENVIRONMENT}")
    logger.info("=" * 52)

    # Initialise database tables (including UserMemory)
    init_db()
    from ai.memory import init_memory_table
    init_memory_table()
    logger.info("Database + memory tables initialised.")

    if not config.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Exiting.")
        sys.exit(1)

    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set. Exiting.")
        sys.exit(1)

    # Build scheduler (needs bot token)
    from telegram import Bot
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    scheduler = BackgroundScheduler(bot)

    # Run FastAPI + Telegram concurrently
    await asyncio.gather(
        run_fastapi(),
        run_telegram_bot(scheduler),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down...")
