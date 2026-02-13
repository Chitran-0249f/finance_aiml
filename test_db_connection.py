from src.db.supabase_client import insert_market_snapshot

insert_market_snapshot({
        "sp_futures": 1.0,
        "dow_futures": 1.0,
        "nasdaq_futures": 1.0,
        "gold": 1.0,
        "crude_oil": 1.0,
        "russell_2000": 1.0,
        "vix": 1.0
})

print("✅ Database insert OK")
