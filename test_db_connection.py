from src.db.supabase_client import insert_market_snapshot

insert_market_snapshot({
    "sp_futures": 1.0,
    "dow_futures": 1.0,
    "nasdaq_futures": 1.0,
    "gold": 1.0,
    "oil": 1.0
})

print("✅ Database insert OK")
