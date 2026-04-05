"""Streamlit app for natural-language querying of the gold layer.

Uses Claude to translate plain-English questions into SQL, executes
them against the gold schema, and displays results with AI-generated
insights and optional charts.
"""

import streamlit as st
import pandas as pd
import anthropic
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from dotenv import load_dotenv
from src.utils.db_connection import get_db_connection


load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

GOLD_SCHEMA = """
gold.dim_date (date_id DATE PK, year INT, quarter INT, month INT, day INT, day_of_week INT, is_weekend BOOL, month_name TEXT, day_name TEXT)

gold.dim_products (dim_product_key INT PK, product_id INT, product_name TEXT, product_slug TEXT, product_price NUMERIC, valid_from TIMESTAMP, valid_to TIMESTAMP, is_current BOOL, product_description TEXT, product_category_id INT, created_at TIMESTAMP, updated_at TIMESTAMP)

gold.dim_customers (dim_customer_key INT PK, customer_id INT, customer_name TEXT, customer_email TEXT, customer_role TEXT, created_at TIMESTAMP, updated_at TIMESTAMP)

gold.fact_orders (fact_order_key INT PK, order_id INT, dim_customer_key INT FK->dim_customers, dim_product_key INT FK->dim_products, quantity INT, unit_price NUMERIC, total_price NUMERIC, order_date DATE FK->dim_date)

Relationships:
- fact_orders.dim_customer_key -> dim_customers.dim_customer_key
- fact_orders.dim_product_key -> dim_products.dim_product_key
- fact_orders.order_date -> dim_date.date_id
- For dim_products, use is_current=TRUE for current product data
"""


def generate_sql(question):
    """Convert a natural-language question into a PostgreSQL SELECT query.

    Sends the gold schema definition and the user's question to Claude,
    which returns a raw SQL string.

    Args:
        question: Plain-English question about the ecommerce data.

    Returns:
        str: A PostgreSQL SELECT query answering the question.
    """
    prompt = f"""You are a SQL expert. Given the following PostgreSQL database schema:

{GOLD_SCHEMA}

Write a SQL query to answer this question: {question}

Rules:
- Return ONLY the SQL query, no explanation, no markdown, no code blocks
- Use PostgreSQL syntax
- Only SELECT queries (no INSERT, UPDATE, DELETE)
- Always use table aliases
- Limit results to 100 rows max
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def run_query(sql):
    """Execute a SQL query against the database and return results as a DataFrame.

    Args:
        sql: A valid PostgreSQL SELECT query string.

    Returns:
        pandas.DataFrame: Query results.
    """
    connection = get_db_connection()
    try:
        df = pd.read_sql(sql, connection)
        return df
    finally:
        connection.close()


def analyze_results(question, sql, df):
    """Generate an AI insight and chart recommendation for query results.

    Sends the original question, executed SQL, and result data to Claude,
    which returns a structured analysis with an insight and chart suggestion.

    Args:
        question: The original natural-language question.
        sql: The SQL query that was executed.
        df: DataFrame containing the query results.

    Returns:
        str: Structured text with INSIGHT, CHART, X_AXIS, and Y_AXIS lines.
    """
    prompt = f"""You are a data analyst. A user asked: "{question}"

This SQL was executed:
{sql}

Here are the results:
{df.to_string(index=False, max_rows=50)}

Provide:
1. A brief insight (2-3 sentences) explaining what the data shows
2. Recommend a chart type: "bar", "line", or "none" (if data isn't suitable for charting)
3. If charting, specify which column is the x-axis and which is the y-axis

Format your response exactly like this:
INSIGHT: your insight here
CHART: bar/line/none
X_AXIS: column_name
Y_AXIS: column_name
"""
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


def parse_analysis(analysis_text):
    """Parse the structured analysis response into a dictionary.

    Args:
        analysis_text: Raw text from analyze_results containing
            INSIGHT, CHART, X_AXIS, and Y_AXIS lines.

    Returns:
        dict: Keys are "insight", "chart", "x_axis", and "y_axis".
    """
    result = {"insight": "", "chart": "none", "x_axis": "", "y_axis": ""}
    for line in analysis_text.split("\n"):
        if line.startswith("INSIGHT:"):
            result["insight"] = line.replace("INSIGHT:", "").strip()
        elif line.startswith("CHART:"):
            result["chart"] = line.replace("CHART:", "").strip().lower()
        elif line.startswith("X_AXIS:"):
            result["x_axis"] = line.replace("X_AXIS:", "").strip()
        elif line.startswith("Y_AXIS:"):
            result["y_axis"] = line.replace("Y_AXIS:", "").strip()
    return result


# Streamlit UI
st.set_page_config(page_title="E-Commerce Analytics AI", layout="wide")
st.title("E-Commerce Analytics AI")
st.markdown("Ask questions about your e-commerce data in natural language.")

question = st.text_input("Ask a question:", placeholder="e.g., What was the total revenue by month?")

if question:
    with st.spinner("Generating SQL..."):
        sql = generate_sql(question)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    try:
        with st.spinner("Running query..."):
            df = run_query(sql)

        st.subheader("Results")
        st.dataframe(df, use_container_width=True)

        if not df.empty:
            with st.spinner("Analyzing results..."):
                analysis = analyze_results(question, sql, df)
                parsed = parse_analysis(analysis)

            st.subheader("Insight")
            st.write(parsed["insight"])

            if parsed["chart"] != "none" and parsed["x_axis"] in df.columns and parsed["y_axis"] in df.columns:
                st.subheader("Visualization")
                chart_data = df.set_index(parsed["x_axis"])[parsed["y_axis"]]
                if parsed["chart"] == "bar":
                    st.bar_chart(chart_data)
                elif parsed["chart"] == "line":
                    st.line_chart(chart_data)
    except Exception as e:
        st.error(f"Error running query: {e}")
