CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE  ,
    name TEXT
);

CREATE TABLE IF NOT EXISTS company_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_code TEXT,
    date TEXT,
    last_trade_price REAL,
    max REAL,
    min REAL,
    avg_price REAL,
    percent_change REAL,
    volume REAL,
    turnover_best_denars REAL,
    total_turnover_denars REAL,
    FOREIGN KEY (company_code) REFERENCES companies(code)
);

