-- USE THIS CODE TO CREATE TABLE IN POSTRGRESS

CREATE TABLE market_snapshots (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    sp_futures DOUBLE PRECISION,
    dow_futures DOUBLE PRECISION,
    nasdaq_futures DOUBLE PRECISION,
    gold DOUBLE PRECISION,
    crude_oil double precision,
    russell_2000 DOUBLE PRECISION,
    vix DOUBLE PRECISION
);


--This file is:
-- For you
-- For rollback
-- For future reference
-- For teams

