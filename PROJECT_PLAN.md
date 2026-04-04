# E-Commerce Data Warehouse Project Plan

## Project Overview
Build a production-ready data warehouse using the Medallion Architecture (Bronze → Silver → Gold) to demonstrate end-to-end data engineering skills. This project will showcase on GitHub for potential clients on Upwork and other platforms.

**Timeline**: ~5 weeks @ 15 hours/week = 75 hours total
**API Source**: Platzi Fake Store API (https://fakeapi.platzi.com)

---

## Learning Objectives

### Core Concepts to Master
1. **Medallion Architecture** - Understanding raw → clean → business-ready data layers
2. **Idempotency** - Pipelines that produce same results when run multiple times
3. **Incremental Loading** - Only processing new/changed data, not full refresh every time
4. **Slowly Changing Dimensions** - Tracking historical changes (e.g., product price changes)
5. **Data Quality at Scale** - Automated validation, not manual checks
6. **Dimensional Modeling** - Star schema with fact and dimension tables

### Technical Skills
- Python for data ingestion (requests, pandas, psycopg2)
- PostgreSQL for storage (DDL, DML, window functions, CTEs)
- Airflow for orchestration
- SQL transformations (not dbt for this project - learn SQL fundamentals first)
- Data quality testing
- Git workflow and documentation

---

## Architecture Design

### Data Layers (Medallion)

#### Bronze Layer (Raw)
**Purpose**: Store exactly what the API returns. Immutable landing zone.
**Schema**: `bronze`
**Tables**:
- `bronze.products_raw` - Raw product data from API
- `bronze.categories_raw` - Raw category data
- `bronze.users_raw` - Raw user data (represents customers)
- `bronze.ingestion_log` - Track what was ingested when

**Key Principles**:
- Store as JSONB or preserve original structure
- Include ingestion metadata (timestamp, source, batch_id)
- Never delete or update - append only
- If API changes schema tomorrow, you have history

#### Silver Layer (Clean)
**Purpose**: Clean, validated, deduplicated data. The "single source of truth."
**Schema**: `silver`
**Tables**:
- `silver.products` - Cleaned products with proper data types
- `silver.categories` - Cleaned categories
- `silver.customers` - Cleaned user/customer data
- `silver.data_quality_checks` - Results of validation tests

**Transformations**:
- Fix data types (strings → numbers, dates)
- Handle nulls (impute or flag)
- Remove duplicates (based on business logic)
- Standardize formats (e.g., phone numbers, addresses)
- Add data quality flags

#### Gold Layer (Business)
**Purpose**: Business-ready analytics tables. Answer specific questions.
**Schema**: `gold`
**Tables**:
- `gold.dim_products` - Product dimension (SCD Type 2 for price changes)
- `gold.dim_customers` - Customer dimension
- `gold.dim_date` - Date dimension
- `gold.fact_orders` - Order transactions (simulated from cart data)
- `gold.fact_daily_sales` - Daily aggregated metrics

**Business Metrics**:
- Daily/Monthly revenue
- Top selling products
- Customer lifetime value
- Inventory turnover
- Category performance

---

## Technology Stack

### Core Infrastructure
- **Database**: PostgreSQL 15+ (local Docker or native install)
- **Language**: Python 3.10+
- **Orchestration**: Apache Airflow 2.8+
- **Version Control**: Git + GitHub

### Python Libraries
```
requests        # API calls
pandas          # Data manipulation
psycopg2-binary # PostgreSQL connector
sqlalchemy      # ORM and connection management
python-dotenv   # Environment variables
apache-airflow  # Workflow orchestration
pytest          # Testing
```

### Tools
- DBeaver or pgAdmin for database exploration
- VS Code with Claude Code extension
- Docker (recommended) or local PostgreSQL

---

## Project Phases (5 Weeks)

### Phase 1: Foundation (Week 1 - 15 hours)
**Goal**: Set up infrastructure and Bronze layer

**Tasks**:
1. Environment setup
   - Install PostgreSQL (Docker recommended)
   - Set up Python virtual environment
   - Create project structure
   
2. Database initialization
   - Create schemas (bronze, silver, gold)
   - Create bronze tables with JSONB columns
   - Create ingestion_log table
   
3. First ingestion script
   - Connect to Platzi API
   - Fetch products, categories, users
   - Insert raw data into bronze layer
   - Log ingestion metadata

**Deliverables**:
- Working PostgreSQL database
- Python script that ingests data into bronze
- Documentation of API endpoints used

**Key Learning**:
- Why separate schemas for each layer?
- Why store raw JSON instead of parsing immediately?
- What is idempotency and why does it matter?

---

### Phase 2: Silver Layer (Week 2 - 15 hours)
**Goal**: Transform bronze → silver with data quality checks

**Tasks**:
1. Create silver tables with proper schemas
   - Define data types based on API response
   - Add created_at, updated_at, is_active columns
   
2. Write transformation SQL
   - Parse JSONB from bronze
   - Cast to proper types
   - Handle NULL values
   - Deduplicate records
   
3. Implement data quality checks
   - Check for NULLs in required fields
   - Validate data ranges (price > 0, dates valid)
   - Identify duplicates
   - Log results to data_quality_checks table
   
4. Make transformations idempotent
   - Use UPSERT (INSERT ... ON CONFLICT)
   - Track processing with watermarks

**Deliverables**:
- Silver layer tables with clean data
- SQL transformation scripts
- Data quality validation framework

**Key Learning**:
- What makes data "clean"?
- How to handle duplicates (which one to keep)?
- Why use UPSERT instead of DELETE + INSERT?
- What's a watermark in data pipelines?

---

### Phase 3: Gold Layer & Business Logic (Week 3 - 15 hours)
**Goal**: Create dimensional model and business metrics

**Tasks**:
1. Design star schema
   - Identify facts (orders) and dimensions (products, customers, date)
   - Implement SCD Type 2 for products (track price changes)
   
2. Generate synthetic order data
   - Create realistic orders based on products and customers
   - Simulate 6 months of transactions
   - Add timestamps to enable time-series analysis
   
3. Build dimension tables
   - dim_products with versioning
   - dim_customers
   - dim_date (complete calendar table)
   
4. Build fact tables
   - fact_orders (grain: one row per order line item)
   - fact_daily_sales (aggregated metrics)
   
5. Create business metric views
   - Monthly revenue by category
   - Top 10 products by sales
   - Customer purchase frequency

**Deliverables**:
- Star schema implementation
- Synthetic order data (5000+ orders)
- SQL queries for business metrics

**Key Learning**:
- What is dimensional modeling (star schema)?
- Why SCD Type 2? When would you use Type 1 or 3?
- What is the "grain" of a fact table?
- How do surrogate keys work?

---

### Phase 4: Orchestration (Week 4 - 15 hours)
**Goal**: Automate pipeline with Airflow

**Tasks**:
1. Set up Airflow
   - Install Airflow locally
   - Configure connections to PostgreSQL
   
2. Create DAGs
   - `dag_bronze_ingestion` - Daily API pull
   - `dag_silver_transform` - Bronze → Silver
   - `dag_gold_build` - Silver → Gold
   
3. Implement dependencies
   - Bronze → Silver → Gold flow
   - Success/failure notifications
   
4. Add monitoring
   - Track run duration
   - Log row counts at each stage
   - Alert on failures
   
5. Schedule and test
   - Set appropriate intervals (daily for bronze)
   - Backfill historical data
   - Test idempotency by running twice

**Deliverables**:
- 3 working Airflow DAGs
- Scheduled pipeline runs
- Monitoring dashboard in Airflow UI

**Key Learning**:
- Why use an orchestrator vs cron jobs?
- What is a DAG (Directed Acyclic Graph)?
- How to handle failures and retries?
- What's backfilling and when do you need it?

---

### Phase 5: Testing, Monitoring & Documentation (Week 5 - 15 hours)
**Goal**: Production-ready code with tests and docs

**Tasks**:
1. Data quality tests
   - Write pytest tests for transformations
   - Implement schema validation
   - Add data freshness checks
   - Test null handling edge cases
   
2. Monitoring setup
   - Row count anomaly detection
   - Data freshness alerts (last ingestion > 25 hours)
   - Failed pipeline notifications
   
3. Documentation
   - Architecture diagram (draw.io or similar)
   - README with setup instructions
   - Each script has docstrings
   - Document design decisions (why PostgreSQL? why not dbt?)
   
4. GitHub preparation
   - Clean up code
   - Remove hardcoded credentials
   - Add .gitignore
   - Write compelling README

**Deliverables**:
- Test suite with >80% coverage
- Monitoring alerts configured
- Complete GitHub repository
- Architecture diagram

**Key Learning**:
- How to test data pipelines?
- What makes data "fresh"?
- How to detect anomalies in data?
- What makes good data engineering documentation?

---

## Project Structure

```
ecommerce-data-warehouse/
├── README.md                          # Main project documentation
├── docs/
│   ├── ARCHITECTURE.md                # System design and diagrams
│   ├── SETUP.md                       # Environment setup guide
│   ├── LEARNING_LOG.md                # Your daily learnings
│   └── diagrams/
│       └── architecture.png           # Visual architecture
├── src/
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── api_client.py              # Platzi API wrapper
│   │   └── bronze_loader.py           # Load raw data to bronze
│   ├── transformations/
│   │   ├── __init__.py
│   │   ├── bronze_to_silver.py        # Cleaning logic
│   │   └── silver_to_gold.py          # Business logic
│   ├── data_quality/
│   │   ├── __init__.py
│   │   ├── validators.py              # Data validation rules
│   │   └── monitors.py                # Anomaly detection
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── db_connection.py           # Database utilities
│   │   └── logger.py                  # Logging setup
│   └── order_generator/
│       └── generate_orders.py         # Synthetic data generator
├── airflow/
│   ├── dags/
│   │   ├── dag_bronze_ingestion.py
│   │   ├── dag_silver_transform.py
│   │   └── dag_gold_build.py
│   └── config/
│       └── airflow.cfg
├── sql/
│   ├── ddl/
│   │   ├── 01_create_schemas.sql
│   │   ├── 02_bronze_tables.sql
│   │   ├── 03_silver_tables.sql
│   │   └── 04_gold_tables.sql
│   ├── transformations/
│   │   ├── bronze_to_silver_products.sql
│   │   ├── bronze_to_silver_customers.sql
│   │   └── silver_to_gold_facts.sql
│   └── queries/
│       ├── business_metrics.sql       # Analytics queries
│       └── data_quality.sql           # Validation queries
├── tests/
│   ├── test_ingestion.py
│   ├── test_transformations.py
│   └── test_data_quality.py
├── config/
│   ├── .env.example                   # Template for environment vars
│   └── database.yml                   # Database connection config
├── requirements.txt
├── .gitignore
└── docker-compose.yml                 # PostgreSQL + Airflow (optional)
```

---

## Platzi API Endpoints

### Available Endpoints
```python
BASE_URL = "https://api.escuelajs.co/api/v1"

# Products
GET /products              # All products
GET /products/{id}         # Single product
GET /products/?limit=10&offset=0  # Pagination

# Categories  
GET /categories            # All categories
GET /categories/{id}       # Single category

# Users (treat as customers)
GET /users                 # All users
GET /users/{id}            # Single user

# Note: API doesn't have orders/carts, you'll generate these
```

### Sample Response Structures
```json
// Product
{
  "id": 1,
  "title": "Product Name",
  "price": 100,
  "description": "Description text",
  "images": ["url1", "url2"],
  "category": {
    "id": 1,
    "name": "Category Name",
    "image": "url"
  },
  "creationAt": "2024-01-01T00:00:00.000Z",
  "updatedAt": "2024-01-01T00:00:00.000Z"
}
```

---

## Data Generation Strategy

Since the API doesn't provide orders/transactions, you'll generate realistic ones:

### Order Generation Logic
```python
# Pseudo-code for order generation
for date in last_6_months:
    num_orders = random(10, 50)  # Vary by day
    for order in num_orders:
        customer = random_choice(customers)
        num_items = random(1, 5)
        for item in num_items:
            product = weighted_random_choice(products)  # Popular products more likely
            quantity = random(1, 3)
            price = product.price  # Use price at that date
```

**Make it realistic**:
- More orders on weekends
- Seasonal patterns (higher in December)
- Some products more popular than others
- Repeat customers (some buy multiple times)
- Price changes over time (track in SCD Type 2)

---

## Key Design Decisions

### Why PostgreSQL (not MySQL, MongoDB)?
- JSONB support for bronze layer (best of both worlds)
- Advanced SQL features (window functions, CTEs, UPSERT)
- Free, open-source, industry standard
- Good for learning SQL fundamentals

### Why No dbt (Initially)?
- First project should teach SQL fundamentals
- dbt abstracts too much for learning
- Better to understand transformations manually first
- You can add dbt later as an enhancement

### Why Generate Orders (not use real API)?
- Learn data modeling from scratch
- Control data quality issues intentionally
- Create realistic time-series patterns
- Shows more engineering thinking

### Why Docker for PostgreSQL?
- Isolated environment
- Easy teardown and rebuild
- Same setup works on any machine
- Good practice for production

---

## Success Criteria

### Technical
- [ ] Bronze layer ingests data from API successfully
- [ ] Silver layer has clean, validated data
- [ ] Gold layer answers business questions
- [ ] Airflow DAGs run on schedule
- [ ] Tests pass with >80% coverage
- [ ] Pipeline is idempotent (can run multiple times safely)

### Learning
- [ ] Can explain medallion architecture to non-technical person
- [ ] Understands when to use each SCD type
- [ ] Can debug failed pipeline runs
- [ ] Knows difference between OLTP and OLAP
- [ ] Can write efficient SQL (avoid SELECT *, use indexes)

### Portfolio
- [ ] GitHub repo with clear README
- [ ] Architecture diagram included
- [ ] Code is well-documented
- [ ] Shows understanding of trade-offs
- [ ] Demonstrates problem-solving (API limitations, data quality)

---

## Common Pitfalls to Avoid

1. **Over-engineering too early**
   - Start simple, add complexity gradually
   - Don't try to build the perfect system on day 1
   
2. **Ignoring data quality**
   - Check for issues early and often
   - Log validation results, don't just print
   
3. **Hardcoding values**
   - Use config files for connection strings
   - Never commit credentials to GitHub
   
4. **Not testing idempotency**
   - Run your pipeline twice on same data
   - Should produce identical results
   
5. **Poor documentation**
   - Future you (and employers) need to understand your code
   - Explain WHY, not just WHAT

---

## Resources for Learning

### Concepts
- Medallion Architecture: [Databricks Guide]
- Dimensional Modeling: "The Data Warehouse Toolkit" by Kimball
- Slowly Changing Dimensions: [SCD Types Explained]
- Idempotency: [Martin Fowler's Article]

### Technical
- PostgreSQL: Official docs + Mode Analytics SQL tutorial
- Airflow: Official tutorial + Astronomer guides
- Python data engineering: "Data Engineering with Python" book

### SQL Practice
- Mode Analytics SQL tutorial (free)
- LeetCode database problems
- Window functions practice on HackerRank

---

## Next Steps

1. **Set up environment** - PostgreSQL, Python, Git
2. **Create SETUP.md** - Document every setup step as you do it
3. **Start Phase 1** - Bronze layer ingestion
4. **Use LEARNING_LOG.md** - Document what you learn daily

**Remember**: The goal is not just to build this, but to LEARN deeply. When you hit a problem:
1. Try to solve it yourself first
2. Document what you tried
3. Ask questions that help you understand WHY
4. Update your learning log

Good luck! 🚀
