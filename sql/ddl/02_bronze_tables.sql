CREATE TABLE IF NOT EXISTS bronze.products_raw (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    products_payload JSONB,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    source TEXT,
    batch_id TEXT);

CREATE TABLE IF NOT EXISTS bronze.categories_raw (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    categories_payload JSONB,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    source TEXT,
    batch_id TEXT);

CREATE TABLE IF NOT EXISTS bronze.users_raw (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    users_payload JSONB,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    source TEXT,
    batch_id TEXT);

CREATE TABLE IF NOT EXISTS bronze.ingestion_log (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source TEXT,
    batch_id TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT NOW(),
    record_count INTEGER,
    status TEXT,
    table_name TEXT,
    error_message TEXT);