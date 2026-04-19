"""
test_smoke.py
─────────────
Smoke test — verifies all modules import cleanly, DB initialises,
and the Gemini client + router are wired correctly.

Run with:  python test_smoke.py
"""
import sys

PASS = "  ✅"
FAIL = "  ❌"

def ok(label):    print(f"{PASS} {label}")
def fail(label, e):
    print(f"{FAIL} {label}: {e}")
    sys.exit(1)

print("\n🔍 Smoke tests (Gemini edition)…\n")

# ── Config ────────────────────────────────────────────────────────────────
try:
    from config import config
    assert config.GEMINI_FLASH_MODEL, "GEMINI_FLASH_MODEL not set"
    ok(f"config  flash={config.GEMINI_FLASH_MODEL}")
except Exception as e:
    fail("config", e)

# ── Database ──────────────────────────────────────────────────────────────
try:
    from db.database import init_db
    from db.models import Portfolio, Trade, DailySnapshot, Signal, LearningLog
    init_db()
    ok("database + models (SQLite OK)")
except Exception as e:
    fail("database", e)

# ── Gemini client ─────────────────────────────────────────────────────────
try:
    from ai.gemini_client import ModelTier, get_quota_stats, parse_json_response
    q = get_quota_stats()
    assert "total_calls" in q
    ok(f"gemini_client  quota_remaining={q['quota_remaining']}")
except Exception as e:
    fail("gemini_client", e)

# ── Router ────────────────────────────────────────────────────────────────
try:
    from ai.router import route_request, RequestTier

    tests = [
        ("hello",                  RequestTier.LITE),
        ("show my pnl",            RequestTier.SKIP),
        ("redesign strategy",      RequestTier.PRO),
        ("analyze BTC momentum",   RequestTier.FLASH),
        ("last 10 trades",         RequestTier.SKIP),
        ("balance",                RequestTier.SKIP),
        ("backtest my strategy",   RequestTier.PRO),
        ("what is your status",    RequestTier.LITE),
    ]
    for txt, expected in tests:
        got = route_request(txt)
        assert got == expected, f"'{txt}' → {got} (expected {expected})"
    ok(f"router  ({len(tests)} routing rules verified)")
except Exception as e:
    fail("router", e)

# ── Memory ────────────────────────────────────────────────────────────────
try:
    from ai.memory import init_memory_table, build_context_block, build_mini_context
    init_memory_table()
    ctx  = build_context_block("smoke_test_user")
    mini = build_mini_context("smoke_test_user")
    assert "[User profile]" in ctx
    ok(f"memory  ctx_len={len(ctx)} mini_len={len(mini)}")
except Exception as e:
    fail("memory", e)

# ── Brain ─────────────────────────────────────────────────────────────────
try:
    from ai.brain import evaluate_signal, explain_trade, _default_skip, _summarise_signal_data
    skip = _default_skip("test")
    assert skip["action"] == "skip"
    summary = _summarise_signal_data({"price": 50000, "rsi": 28, "signal": "oversold"}, "crypto")
    assert "price=" in summary
    ok("brain  (_default_skip + _summarise_signal_data OK)")
except Exception as e:
    fail("brain", e)

# ── Markets ───────────────────────────────────────────────────────────────
try:
    from markets import polymarket, crypto, sports, weather_news
    ok("markets (polymarket, crypto, sports, weather_news)")
except Exception as e:
    fail("markets", e)

# ── Strategies ────────────────────────────────────────────────────────────
try:
    from strategies.engine import STRATEGIES, run_strategy
    ok(f"strategies  ({len(STRATEGIES)} loaded: {', '.join(STRATEGIES)})")
except Exception as e:
    fail("strategies", e)

# ── Paper trader ──────────────────────────────────────────────────────────
try:
    from trading.paper_trader import PaperTrader
    trader = PaperTrader("smoke_test_user")
    dash   = trader.get_dashboard()
    ok(f"paper_trader  balance=${dash.get('balance', 0):,.2f}")
except Exception as e:
    fail("paper_trader", e)

# ── Auto closer ───────────────────────────────────────────────────────────
try:
    from trading.auto_closer import check_and_close_trades
    ok("auto_closer")
except Exception as e:
    fail("auto_closer", e)

# ── Learning ──────────────────────────────────────────────────────────────
try:
    from learning.daily_review import get_strategy_performance_summary
    ok("learning.daily_review")
except Exception as e:
    fail("learning", e)

# ── FastAPI ───────────────────────────────────────────────────────────────
try:
    from api.server import app
    routes = [r.path for r in app.routes]
    assert "/api/ai/quota"  in routes, "/api/ai/quota missing"
    assert "/api/ai/models" in routes, "/api/ai/models missing"
    ok(f"api.server  {len(routes)} routes (quota + models present)")
except Exception as e:
    fail("api.server", e)

# ── Bot handlers ──────────────────────────────────────────────────────────
try:
    from bot.handlers import build_application
    ok("bot.handlers  (importable)")
except Exception as e:
    fail("bot.handlers", e)

# ── Notifications ─────────────────────────────────────────────────────────
try:
    from bot.notifications import NotificationService, BackgroundScheduler
    ok("bot.notifications")
except Exception as e:
    fail("bot.notifications", e)

# ── No Anthropic / OpenAI in ai/ layer ───────────────────────────────────
try:
    import pathlib
    ai_files = list(pathlib.Path("ai").glob("*.py"))
    for f in ai_files:
        src = f.read_text().lower()
        assert "anthropic"  not in src, f"{f}: 'anthropic' found"
        assert "openai"     not in src, f"{f}: 'openai' found"
        assert "claude-"    not in src, f"{f}: 'claude-' model string found"
    ok(f"no-legacy-ai  ({len(ai_files)} ai/*.py files — no Anthropic/OpenAI refs)")
except Exception as e:
    fail("no-legacy-ai", e)

# ── JSON parse helper ─────────────────────────────────────────────────────
try:
    from ai.gemini_client import parse_json_response
    good  = parse_json_response('{"action": "buy", "confidence": 0.8}')
    fenced = parse_json_response('```json\n{"action": "skip"}\n```')
    assert good   and good["action"]   == "buy"
    assert fenced and fenced["action"] == "skip"
    assert parse_json_response("not json") is None
    ok("parse_json_response  (valid / fenced / invalid all handled)")
except Exception as e:
    fail("parse_json_response", e)

print("\n" + "="*50)
print("✅ All smoke tests passed!")
print("="*50)
print()
print("Setup steps:")
print("  1.  cp .env.example .env")
print("  2.  Fill in TELEGRAM_BOT_TOKEN + GEMINI_API_KEY")
print("  3.  python main.py")
print("  4.  Send /start to your bot")
print()
print("Model tiers active:")
print(f"  🟡 Lite  → {config.GEMINI_LITE_MODEL}")
print(f"  🟠 Flash → {config.GEMINI_FLASH_MODEL}")
print(f"  🔴 Pro   → {config.GEMINI_PRO_MODEL}")
print(f"  📊 Limit → {config.GEMINI_DAILY_CALL_LIMIT} calls/day")
print()
