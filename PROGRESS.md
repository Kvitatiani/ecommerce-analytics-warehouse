# Project Progress

## Week 1 — Bronze Layer

### Done (Day 1 — 2026-04-04/05)
- [x] PostgreSQL 15 running in Docker (`docker-compose.yml` + `.env`)
- [x] Created schemas: bronze, silver, gold
- [x] Created bronze tables: products_raw, categories_raw, users_raw, ingestion_log
- [x] SQL DDL files: `sql/ddl/01_create_schemas.sql`, `sql/ddl/02_bronze_tables.sql`
- [x] Python virtual environment + installed requests, psycopg2-binary, python-dotenv
- [x] `src/utils/db_connection.py` — database connection utility
- [x] `src/ingestion/api_client.py` — generic API client for Platzi endpoints
- [x] `src/ingestion/bronze_loader.py` — inserts API data into bronze + logs to ingestion_log
- [x] Successfully ingested categories into bronze.categories_raw

### Next Up
- [ ] Ingest products and users (reuse bronze_loader for all three endpoints)
- [ ] Refactor bronze_loader to handle all tables in one run (not hardcoded to categories)
- [ ] Verify ingestion_log is capturing runs correctly
- [ ] Test idempotency — run pipeline twice, check what happens
- [ ] Add `NOT NULL` constraints where appropriate on bronze tables
- [ ] Document API endpoints and response structures
