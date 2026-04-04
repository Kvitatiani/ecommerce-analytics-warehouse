# Quick Start Guide

## Immediate Next Steps

### 1. Copy These Files to Your Project
Move these files from this chat to your actual project directory in VS Code:
- `PROJECT_PLAN.md` - Your complete roadmap
- `CLAUDE.md` - Instructions for Claude Code
- This file (`QUICKSTART.md`)

### 2. Set Up Your Environment

#### Option A: Docker (Recommended)
```bash
# Create docker-compose.yml
# Claude Code will help you with this

docker-compose up -d  # Start PostgreSQL
```

#### Option B: Local PostgreSQL
```bash
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql
sudo service postgresql start

# Windows
# Download from postgresql.org
```

### 3. Create Project Structure
```bash
mkdir -p ecommerce-data-warehouse/{src,sql,airflow,tests,config,docs}
cd ecommerce-data-warehouse
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Test API Connection
Quick test to ensure Platzi API works:
```python
import requests

response = requests.get("https://api.escuelajs.co/api/v1/products?limit=5")
print(f"Status: {response.status_code}")
print(f"Products: {len(response.json())}")
```

### 5. First Session with Claude Code

Ask Claude Code to help you with:
1. "Help me create a docker-compose.yml for PostgreSQL"
2. "Let's create the bronze schema in PostgreSQL"
3. "Explain how we'll structure the ingestion script"

## Week 1 Checklist (Bronze Layer)

### Day 1: Setup (3 hours)
- [ ] PostgreSQL running (verify with `psql -l`)
- [ ] Python virtual environment created
- [ ] Can connect to database from Python
- [ ] Created all three schemas: bronze, silver, gold
- [ ] Document setup steps in `docs/SETUP.md`

### Day 2-3: Bronze Tables & Ingestion (6 hours)
- [ ] Create bronze layer tables (JSONB columns)
- [ ] Create ingestion_log table
- [ ] Write Python script to fetch products from API
- [ ] Store raw JSON in bronze.products_raw
- [ ] Add ingestion metadata (timestamp, batch_id)

### Day 4-5: Complete Bronze Layer (6 hours)
- [ ] Fetch categories, users from API
- [ ] Store in bronze.categories_raw, bronze.users_raw
- [ ] Add error handling to ingestion script
- [ ] Make script idempotent (can run multiple times)
- [ ] Test with various scenarios (API down, duplicate runs)
- [ ] Update LEARNING_LOG.md with lessons learned

## Essential Commands

### PostgreSQL
```bash
# Connect to database
psql -U postgres

# List databases
\l

# Connect to specific database
\c warehouse

# List tables in current schema
\dt bronze.*

# Describe table
\d bronze.products_raw

# Run SQL file
psql -U postgres -d warehouse -f sql/ddl/01_create_schemas.sql
```

### Python Environment
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt

# Run script
python src/ingestion/bronze_loader.py
```

### Git
```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: project structure"

# Don't commit credentials!
echo "*.env" >> .gitignore
echo "venv/" >> .gitignore
```

## Key Concepts to Understand (Week 1)

### 1. Why Bronze Layer?
**Question for yourself**: If the API changes its schema tomorrow, how does bronze protect us?

**Answer**: Bronze stores raw JSON exactly as received. If API adds new field "discountPrice" tomorrow, bronze automatically captures it. Silver layer can then be updated to use it.

### 2. What is Idempotency?
**Test**: Run your ingestion script twice. Does it create duplicate data?

**Goal**: Running same script on same date should produce same result. Use:
- Unique constraints
- UPSERT (INSERT ... ON CONFLICT)
- Batch IDs to track what's processed

### 3. Why Separate Schemas?
**Think about**: What if someone accidentally drops a table?

**Safety**: Separate schemas = separate permissions. Bronze is append-only. Silver/Gold can be rebuilt from bronze if corrupted.

## Your Learning Log Template

Start `docs/LEARNING_LOG.md` with:
```markdown
# Data Warehouse Learning Log

## Week 1: Bronze Layer

### 2025-04-04
**Time spent**: 3 hours
**Focus**: Environment setup

#### What I built
- [ ] List specific accomplishments

#### Concepts learned
**Topic**: [e.g., JSONB vs JSON in PostgreSQL]
- Definition:
- Why it matters:
- When to use:

#### Problems encountered
**Issue**: [Describe the problem]
- What I tried:
- How I solved it:
- What I learned:

#### Questions for later
- [ ] Unanswered question 1
- [ ] Unanswered question 2

#### Next session plan
- Task 1
- Task 2
```

## Common First-Week Issues

### Issue: "Can't connect to PostgreSQL"
**Check**:
1. Is PostgreSQL running? (`pg_isready`)
2. Correct port? (Default: 5432)
3. Correct password in .env file?
4. Firewall blocking connection?

### Issue: "API returns 429 Too Many Requests"
**Solution**: Add delay between requests
```python
import time
time.sleep(1)  # Wait 1 second between calls
```

### Issue: "How much should I do myself vs ask Claude?"
**Guideline**:
- Try for 15-20 minutes first
- Document what you tried
- Then ask Claude with specific question
- Example: "I tried X and Y, got error Z, what concept am I missing?"

## Resources for Week 1

### PostgreSQL
- [Official Docs - JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL Tutorial - Getting Started](https://www.postgresqltutorial.com/)

### Python
- [Requests Documentation](https://requests.readthedocs.io/)
- [Psycopg2 Tutorial](https://www.psycopg.org/docs/usage.html)

### Concepts
- [What is ETL?](https://www.ibm.com/topics/etl)
- [Medallion Architecture Explained](https://www.databricks.com/glossary/medallion-architecture)

## Tips for Success

### 1. Daily Commits
Commit code every day, even if not perfect:
```bash
git commit -m "WIP: bronze ingestion script - added error handling"
```

### 2. Document Decisions
In your learning log, write WHY you chose approaches:
- "Used JSONB instead of JSON because JSONB is faster for queries"
- "Chose psycopg2 over SQLAlchemy to learn SQL fundamentals first"

### 3. Test Everything Twice
Run your ingestion script twice on purpose. Does it:
- Create duplicates? (Bad - not idempotent)
- Update existing? (Good - using UPSERT)
- Throw errors? (Bad - needs better duplicate handling)

### 4. Ask "What If" Questions
- What if API is down during ingestion?
- What if product_id changes from integer to string?
- What if we need to re-process last week's data?

These questions lead to robust design.

## Week 1 Success Criteria

You're ready for Week 2 (Silver Layer) when:
- [ ] Bronze tables exist with data
- [ ] Can query products: `SELECT * FROM bronze.products_raw LIMIT 5;`
- [ ] Understand why we store raw JSON
- [ ] Can explain idempotency to a friend
- [ ] Ingestion script has error handling
- [ ] Learning log has detailed notes
- [ ] Setup process documented in SETUP.md

## Getting Unstuck

If you're stuck for >30 minutes:
1. Document what you've tried in learning log
2. Simplify the problem (test smaller piece)
3. Check PostgreSQL logs
4. Ask Claude Code with context: "Here's what I tried..."
5. Take a break - sometimes the answer comes when you step away

## Remember

This is a learning project, not a race. The goal is to understand:
- **Why** medallion architecture exists
- **How** to handle real-world data messiness  
- **When** to use different patterns

Speed comes with practice. Focus on depth now.

---

**Ready to start?** Copy these files to your project, activate your virtual environment, and ask Claude Code: "Let's set up PostgreSQL and create our first bronze table."

Good luck! 🚀
