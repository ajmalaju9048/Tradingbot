"""
Central configuration for the AI Trading Bot.
AI provider: Google Gemini (three-tier model routing for cost optimisation).
All secrets are loaded from environment variables.
"""
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    # ── Telegram ──────────────────────────────────────────────
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    ADMIN_CHAT_IDS: list = field(
        default_factory=lambda: [
            int(x) for x in os.getenv("ADMIN_CHAT_IDS", "").split(",") if x.strip()
        ]
    )

    # ── Gemini AI (sole provider) ─────────────────────────────
    # Get key at: https://aistudio.google.com/app/apikey
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Three model tiers — swap names here to upgrade/downgrade globally
    # Tier 1 — Fast Chat: greetings, lookups, simple commands
    GEMINI_LITE_MODEL: str = os.getenv(
        "GEMINI_LITE_MODEL", "gemini-2.5-flash-lite-preview-06-17"
    )
    # Tier 2 — Standard: trade analysis, market comparison, reasoning
    GEMINI_FLASH_MODEL: str = os.getenv(
        "GEMINI_FLASH_MODEL", "gemini-2.5-flash-preview-05-20"
    )
    # Tier 3 — Deep: strategy redesign, multi-market reasoning, backtests
    GEMINI_PRO_MODEL: str = os.getenv(
        "GEMINI_PRO_MODEL", "gemini-2.5-pro-preview-06-05"
    )

    # Max output tokens per tier (keeps costs predictable)
    GEMINI_LITE_MAX_TOKENS: int = 256
    GEMINI_FLASH_MAX_TOKENS: int = 512
    GEMINI_PRO_MAX_TOKENS: int = 1024

    # Retry / rate-limit settings
    GEMINI_MAX_RETRIES: int = 3
    GEMINI_RETRY_DELAY: float = 2.0        # seconds between retries
    GEMINI_TIMEOUT: float = 30.0           # per-request timeout

    # Daily quota guard — stop AI calls above this (0 = unlimited)
    GEMINI_DAILY_CALL_LIMIT: int = int(os.getenv("GEMINI_DAILY_CALL_LIMIT", "500"))

    # ── Market APIs ───────────────────────────────────────────
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_SECRET: str = os.getenv("BINANCE_SECRET", "")
    ODDS_API_KEY: str = os.getenv("ODDS_API_KEY", "")          # the-odds-api.com
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    TWITTER_BEARER_TOKEN: str = os.getenv("TWITTER_BEARER_TOKEN", "")

    # ── Polymarket ────────────────────────────────────────────
    POLYMARKET_API_URL: str = "https://clob.polymarket.com"
    POLYMARKET_GAMMA_URL: str = "https://gamma-api.polymarket.com"
    POLYMARKET_PRIVATE_KEY: Optional[str] = os.getenv("POLYMARKET_PRIVATE_KEY")

    # ── Database ──────────────────────────────────────────────
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./trading_bot.db")

    # ── FastAPI ───────────────────────────────────────────────
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("PORT", "8000"))

    # ── Paper Trading ─────────────────────────────────────────
    PAPER_TRADING_INITIAL_BALANCE: float = 1000.0
    MAX_POSITION_SIZE_PCT: float = 0.10    # max 10 % of portfolio per trade
    MAX_DAILY_LOSS_PCT: float = 0.05       # stop trading if −5 % in a day
    MIN_CONFIDENCE: float = 0.60           # minimum AI confidence to trade

    # ── Strategy ──────────────────────────────────────────────
    DEFAULT_STRATEGY: str = os.getenv("DEFAULT_STRATEGY", "momentum")
    AVAILABLE_STRATEGIES: list = field(default_factory=lambda: [
        "momentum", "mean_reversion", "news_based",
        "whale_tracking", "arbitrage", "probability_mismatch", "sentiment",
    ])

    # ── Scheduler ─────────────────────────────────────────────
    SCAN_INTERVAL_SECONDS: int = int(os.getenv("SCAN_INTERVAL_SECONDS", "300"))
    DAILY_REVIEW_HOUR: int = 23    # 11 PM UTC

    # ── Misc ──────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")


config = Config()
