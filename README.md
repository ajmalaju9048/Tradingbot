# 🤖 AI Trading Assistant Bot

A production-ready Telegram bot powered by Claude AI that paper-trades across
**Polymarket prediction markets**, **Crypto (Binance)**, **Sports betting**, and
**Weather markets** — with 7 strategy modes, full P&L tracking, and daily self-learning.

---

## ✨ Feature Overview

| Feature | Details |
|---|---|
| 🧠 AI Brain | Claude / GPT-4 / Gemini decision engine |
| 📊 Markets | Polymarket · Binance · Sports Odds · Weather |
| 📝 Paper Trading | Virtual $1,000 · risk management · auto SL/TP |
| 🎯 Strategies | Momentum · Mean Reversion · News · Whale · Arbitrage · Prob-Mismatch · Sentiment |
| 📅 Daily Review | AI reviews trades nightly and auto-improves |
| 🔔 Alerts | Proactive Telegram push notifications |
| 🌐 REST API | FastAPI dashboard backend |
| 🗃️ Database | SQLite (dev) / PostgreSQL (prod) |
| 🚀 Deploy | Railway · Render · Replit one-click |

---

## 📁 Project Structure

```
trading-bot/
├── main.py                     # Entry point (bot + API together)
├── config.py                   # All config (env vars)
├── requirements.txt
├── .env.example                # Copy → .env
├── railway.toml                # Railway deploy config
├── render.yaml                 # Render deploy config
│
├── bot/
│   ├── handlers.py             # Telegram commands & text handler
│   └── notifications.py       # Proactive alerts + background scheduler
│
├── ai/
│   └── brain.py                # Claude/GPT/Gemini decision engine
│
├── strategies/
│   └── engine.py               # All 7 strategies + registry
│
├── trading/
│   ├── paper_trader.py         # Paper trading + portfolio
│   └── auto_closer.py          # Auto stop-loss / take-profit
│
├── markets/
│   ├── polymarket.py           # Polymarket CLOB + Gamma API
│   ├── crypto.py               # Binance REST + TA indicators
│   ├── sports.py               # The-Odds-API (mispricing detection)
│   └── weather_news.py         # OpenWeather + NewsAPI + Twitter
│
├── learning/
│   └── daily_review.py         # Nightly AI review + strategy rotation
│
├── api/
│   └── server.py               # FastAPI REST endpoints
│
└── db/
    ├── models.py               # SQLAlchemy models
    └── database.py             # Engine + session factory
```

---

## 🚀 Quick Start — Local

### Step 1 — Clone & install

```bash
git clone https://github.com/yourname/ai-trading-bot
cd ai-trading-bot
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Create your Telegram bot

1. Open Telegram → search **@BotFather**
2. Send `/newbot` → follow prompts → copy your **bot token**
3. Send `/start` to your new bot to get your **chat ID**
   (or use **@userinfobot** to find your user ID)

### Step 3 — Configure environment

```bash
cp .env.example .env
```

Edit `.env` — minimum required fields:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHI...    # from BotFather
ADMIN_CHAT_IDS=123456789                       # your Telegram user ID
ANTHROPIC_API_KEY=sk-ant-...                   # from console.anthropic.com
```

Optional (bot works without these, uses mock data):

```env
ODDS_API_KEY=...          # the-odds-api.com — free tier
OPENWEATHER_API_KEY=...   # openweathermap.org — free tier
NEWS_API_KEY=...          # newsapi.org — free tier
TWITTER_BEARER_TOKEN=...  # developer.twitter.com
```

### Step 4 — Run

```bash
python main.py
```

You should see:
```
==================================================
  AI Trading Bot — Starting up
  AI Provider : anthropic
  Strategy    : momentum
  Environment : production
==================================================
Database initialised.
Telegram bot started (polling).
```

Open Telegram → send `/start` to your bot 🎉

---

## 💬 Bot Commands

### Market Analysis
| Command | Description |
|---|---|
| `/analyze` | Scan markets with current strategy, get AI decisions |
| `/news` | Latest market-moving headlines |
| `/weather` | Extreme weather events (weather market signals) |
| `/sports` | Sports betting mispricings across all leagues |

### Paper Trading
| Command | Description |
|---|---|
| `/papertrade` | Run one full trading cycle (scan → AI decide → place trades) |
| `/current_positions` | Full portfolio dashboard (P&L, win rate, open trades) |

### Strategy
| Command | Description |
|---|---|
| `/strategy` | Show current strategy + tap buttons to change |
| `/change_strategy momentum` | Switch strategy by name |

### Free-Text Admin Chat
Just type natural language — the AI will answer:

```
You: What strategy are you using?
Bot: Currently using momentum strategy with 67% win rate...

You: Change strategy to whale tracking
Bot: ✅ Strategy changed to whale_tracking

You: Show last 20 trades
Bot: [formatted trade history]

You: Why did you take the last trade?
Bot: The Bitcoin position was opened because RSI dropped to 28...

You: Best performing market?
Bot: Crypto markets have generated the highest P&L (67%) this week...
```

---

## 🧠 Strategy Details

| Strategy | Signal Source | Best For |
|---|---|---|
| `momentum` | RSI, MACD, 24h price change | Trending crypto markets |
| `mean_reversion` | RSI extremes (<30 / >70) | Sideways markets |
| `news_based` | NewsAPI keyword detection | Event-driven markets |
| `whale_tracking` | Large Polymarket trades (>$500) | Following smart money |
| `arbitrage` | YES+NO price gap >3% | Risk-free Polymarket plays |
| `probability_mismatch` | Cross-bookie odds divergence | Sports betting edges |
| `sentiment` | Twitter bullish/bearish score | Social-driven assets |
| `weather_event` | Temperature/wind/rain extremes | Weather prediction markets |

---

## 📊 REST API Endpoints

Once running, the FastAPI server is at `http://localhost:8000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api/portfolio/{user_id}` | Full portfolio dashboard |
| GET | `/api/portfolio/{user_id}/trades` | Trade history |
| GET | `/api/portfolio/{user_id}/pnl_chart` | Daily P&L series |
| POST | `/api/portfolio/{user_id}/strategy` | Change strategy |
| POST | `/api/trades/{trade_id}/close` | Manually close trade |
| GET | `/api/learning/logs` | Daily AI review logs |
| GET | `/api/stats` | Global bot statistics |
| GET | `/docs` | Swagger UI |

---

## 🌍 Deployment

### Option A — Railway (Recommended, free tier)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Select your repo
4. Go to **Variables** → add all your `.env` values
5. Railway auto-detects `railway.toml` and deploys

```
✅ Free tier: 500 hours/month
✅ Automatic HTTPS
✅ Persistent storage (add PostgreSQL plugin)
```

### Option B — Render (Free tier)

1. Push to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo — Render auto-reads `render.yaml`
4. Add environment variables in the dashboard
5. Deploy

```
✅ Free tier: sleeps after 15min idle (use cron ping to keep alive)
✅ PostgreSQL add-on available
```

### Option C — Replit

1. Create new Replit → import from GitHub
2. In **Secrets** tab, add all your `.env` values
3. Click **Run**

```
✅ Always-on with Replit Core ($7/mo)
✅ Built-in database available
```

### PostgreSQL for Production

Replace the `DATABASE_URL` in your environment:

```env
DATABASE_URL=postgresql://user:password@host:5432/trading_bot
```

Railway and Render both offer free PostgreSQL add-ons. The code handles both
SQLite and PostgreSQL automatically.

---

## 🔔 Notification System

The bot sends **proactive alerts** — you don't need to run commands:

| Alert Type | Trigger |
|---|---|
| 📡 New Trade Signal | Any signal with confidence > 60% |
| 🚀 High Prob Trade | Confidence > 80% |
| 🌩 Weather Event | Extreme weather in monitored cities |
| ⚽ Sports Mispricing | Edge > 5% vs consensus |
| 🚀 Crypto Breakout | Momentum signal on BTCUSDT / ETHUSDT etc. |
| 📅 Daily Review | Every night at 11 PM UTC |

**Scan intervals:**
- Market scan: every 5 minutes (configurable via `SCAN_INTERVAL_SECONDS`)
- Crypto watchdog: every 10 minutes
- Weather watchdog: every 30 minutes
- Sports watchdog: every 15 minutes
- Daily review: 11 PM UTC

---

## 🛡️ Risk Management

Built-in risk controls (tunable in `config.py`):

| Rule | Default |
|---|---|
| Max position size | 10% of portfolio |
| Daily loss limit | Stop trading if -5% for the day |
| Min AI confidence to trade | 60% |
| Auto stop-loss | 10% below entry |
| Auto take-profit | 20% above entry |
| Stale trade auto-close | 7 days |
| Min balance to trade | $50 |

---

## 🔑 API Keys — Where to Get Them

| Key | Where | Free Tier |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | @BotFather on Telegram | ✅ Free |
| `ANTHROPIC_API_KEY` | console.anthropic.com | $5 credit |
| `OPENAI_API_KEY` | platform.openai.com | $5 credit |
| `ODDS_API_KEY` | the-odds-api.com | 500 req/mo |
| `OPENWEATHER_API_KEY` | openweathermap.org | 1,000 req/day |
| `NEWS_API_KEY` | newsapi.org | 100 req/day |
| `TWITTER_BEARER_TOKEN` | developer.twitter.com | Free basic |

**Note:** The bot works in demo mode without any optional keys — it uses
realistic mock data so you can test everything immediately.

---

## 🧪 Testing Without API Keys

The bot degrades gracefully:
- **No `ODDS_API_KEY`** → uses mock sports data with a realistic mispricing example
- **No `OPENWEATHER_API_KEY`** → returns mock weather for each city
- **No `NEWS_API_KEY`** → returns 2 sample articles
- **No `TWITTER_BEARER_TOKEN`** → sentiment returns "unknown"
- **No `BINANCE_*` keys** → public Binance market data (no auth needed for reads)
- **No Polymarket key** → public Polymarket data (no auth needed for reads)

---

## 🛠️ Customisation

### Add a new strategy

1. Open `strategies/engine.py`
2. Create a new class inheriting `BaseStrategy`
3. Implement the `scan()` method returning a list of signal dicts
4. Register it in `STRATEGIES` dict
5. Add it to `AVAILABLE_STRATEGIES` in `config.py`

### Change risk parameters

Edit `config.py`:
```python
MAX_POSITION_SIZE_PCT = 0.10   # 10% max per trade
MAX_DAILY_LOSS_PCT    = 0.05   # stop after -5% daily loss
MIN_CONFIDENCE        = 0.60   # require 60%+ AI confidence
```

### Add a new market

Create a new file in `markets/` with async functions that return signal dicts,
then import it into the appropriate strategy in `strategies/engine.py`.

---

## 📦 Tech Stack

| Component | Technology |
|---|---|
| Bot framework | python-telegram-bot 21 |
| Web framework | FastAPI + Uvicorn |
| AI | Anthropic Claude / OpenAI / Gemini |
| HTTP client | httpx (async) |
| Database | SQLAlchemy 2 + SQLite/PostgreSQL |
| Data models | Pydantic v2 |
| Deployment | Railway / Render / Replit |

---

## ⚠️ Disclaimer

This bot is for **educational and entertainment purposes only**.
Paper trading uses simulated money — no real funds are at risk unless you
explicitly integrate a live exchange account.
Never invest money you cannot afford to lose.
Prediction markets and crypto carry substantial risk.
