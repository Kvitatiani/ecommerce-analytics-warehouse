# Data Warehouse Learning Log

> **Purpose**: Document what you learn, problems you solve, and concepts you master. This becomes your personal knowledge base and interview prep material.

---

## Week 1: Foundation & Bronze Layer

### 2025-04-04: Environment Setup
**Time**: ___ hours | **Phase**: Setup

#### 🎯 What I Built
- 
- 
- 

#### 📚 Concepts Learned

**Topic**: [e.g., PostgreSQL Schemas]
- **What it is**: 
- **Why it matters**: 
- **When to use it**: 
- **Trade-offs**: 

**Topic**: [e.g., JSONB in PostgreSQL]
- **What it is**: 
- **Why it matters**: 
- **When to use it**: 
- **Trade-offs**: 

#### 🐛 Problems Encountered

**Problem**: [Short description]
- **Context**: What I was trying to do
- **Error/Issue**: Exact error message or unexpected behavior
- **What I tried**: 
  1. First attempt
  2. Second attempt
  3. What finally worked
- **Root cause**: Why it happened
- **Lesson**: What this taught me
- **Prevention**: How to avoid in future

#### ❓ Questions Still Unclear
- [ ] Question 1
- [ ] Question 2
- [ ] Question 3

#### 📝 Notes & Insights
- 
- 
- 

#### ✅ Tomorrow's Plan
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

---

### 2025-04-05: [Session Title]
**Time**: ___ hours | **Phase**: Bronze Layer

#### 🎯 What I Built


#### 📚 Concepts Learned


#### 🐛 Problems Encountered


#### ❓ Questions Still Unclear


#### 📝 Notes & Insights


#### ✅ Tomorrow's Plan


---

## Week 2: Silver Layer Transformations

### 2025-04-XX: [Session Title]
**Time**: ___ hours | **Phase**: Silver Layer

[Use same template as above]

---

## Key Learnings Summary

### Medallion Architecture
**Understanding evolved from**: 
- Week 1: "It's three layers for organizing data"
- Week 2: "Bronze protects against schema changes, Silver ensures quality, Gold serves business"
- Week 3: "It's about separation of concerns - raw preservation vs validation vs analytics"

### Idempotency
**Understanding evolved from**:
- Week 1: 
- Week 2: 
- Week 3: 

### Data Quality
**Understanding evolved from**:
- Week 1: 
- Week 2: 
- Week 3: 

---

## Debugging Patterns I've Learned

### Pattern: PostgreSQL Connection Issues
**Symptoms**: 
**Check**:
1. 
2. 
3. 

### Pattern: API Rate Limiting
**Symptoms**:
**Solution**:

### Pattern: UPSERT Not Working
**Symptoms**:
**Common causes**:
**Fix**:

---

## SQL Patterns I've Mastered

### UPSERT Pattern
```sql
-- Example with explanation
INSERT INTO silver.products (id, name, price)
VALUES (1, 'Product', 100)
ON CONFLICT (id) 
DO UPDATE SET 
    name = EXCLUDED.name,
    price = EXCLUDED.price,
    updated_at = NOW();
```
**When to use**: 
**Why it works**: 

### Window Functions
```sql
-- Example
SELECT 
    product_id,
    price,
    LAG(price) OVER (PARTITION BY product_id ORDER BY date) as previous_price
FROM silver.products;
```
**When to use**:
**Why it works**:

---

## Python Patterns I've Mastered

### Database Connection with Context Manager
```python
# Example
with psycopg2.connect(**db_config) as conn:
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
```
**Why this pattern**: 
**What it prevents**: 

### Error Handling in Data Pipelines
```python
# Example
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    # Handle timeout
except requests.HTTPError as e:
    # Handle HTTP errors
```
**Why critical**: 
**What I learned**: 

---

## Design Decisions & Rationale

### Decision: PostgreSQL vs MySQL
**Choice**: PostgreSQL
**Reason**: 
**Trade-off**: 

### Decision: JSONB vs Parsing to Columns in Bronze
**Choice**: JSONB
**Reason**: 
**Trade-off**: 

### Decision: When to use UPSERT vs DELETE+INSERT
**Choice**: 
**Reason**: 
**Trade-off**: 

---

## Interview Prep: Questions I Can Answer

### Can you explain the medallion architecture?
**My answer**:
[Write in your own words]

### How do you ensure data quality in a pipeline?
**My answer**:

### What is idempotency and why does it matter?
**My answer**:

### Tell me about a challenging bug you fixed
**Story**:
- **Situation**: 
- **Problem**: 
- **What I tried**: 
- **Solution**: 
- **What I learned**: 

---

## Resources That Helped

### Articles/Blogs
- [Title](URL) - What I learned:
- [Title](URL) - What I learned:

### Documentation
- PostgreSQL JSONB docs - Helped me understand:
- Airflow DAG docs - Clarified:

### Videos/Tutorials
- [Title](URL) - Key takeaway:

---

## Progress Tracking

### Week 1 Goals
- [x] Completed goal 1
- [x] Completed goal 2  
- [ ] In progress goal 3

### Week 2 Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

### Overall Project Status
**Completed**: Bronze layer ingestion
**In Progress**: Silver transformations
**Blocked**: None
**Next Up**: Gold dimensional modeling

---

## Reflections

### What's Going Well
- 

### What's Challenging
- 

### What I'd Do Differently
- 

### Surprising Discoveries
- 

---

## Code Snippets Worth Saving

### [Snippet Name]
```python
# Code here
```
**Why it's useful**: 
**When to use**: 

---

## Glossary (Terms I've Learned)

**Idempotency**: 
**Medallion Architecture**: 
**SCD Type 2**: 
**UPSERT**: 
**JSONB**: 
**Star Schema**: 
**Fact Table**: 
**Dimension Table**: 
**ETL**: 
**DAG**: 

---

*Last Updated*: [Date]
*Current Phase*: [Bronze/Silver/Gold/Orchestration/Testing]
*Next Milestone*: [What you're working toward]
