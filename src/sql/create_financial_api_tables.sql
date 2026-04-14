
-- Stores raw API JSON for ALL statements (debugging + audit)
CREATE TABLE financial_statements_raw (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- unique row ID

    symbol TEXT,
    -- stock ticker

    statement_type TEXT,
    -- income / balance / cashflow

    data JSONB,
    -- full JSON stored exactly as received

    created_at TIMESTAMP DEFAULT NOW()
    -- timestamp
);








CREATE TABLE financial_reports (

    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    symbol TEXT,
    report_date DATE,
    period TEXT
);





CREATE TABLE income_statements (

    report_id BIGINT REFERENCES financial_reports(id),

    revenue BIGINT,
    net_income BIGINT,
    gross_profit BIGINT,
    eps NUMERIC,

    PRIMARY KEY (report_id)
);









CREATE TABLE balance_sheets (

    report_id BIGINT REFERENCES financial_reports(id),

    total_assets BIGINT,
    total_liabilities BIGINT,
    total_equity BIGINT,
    total_debt BIGINT,

    PRIMARY KEY (report_id)
);








CREATE TABLE cash_flows (

    report_id BIGINT REFERENCES financial_reports(id),

    operating_cash_flow BIGINT,
    free_cash_flow BIGINT,
    capital_expenditure BIGINT,

    PRIMARY KEY (report_id)
);