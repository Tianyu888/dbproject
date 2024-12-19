import json
import openai
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.shortcuts import render

prompt = f"""
    You are working with a relational database. Below is the database schema and additional instructions for generating SQL queries. Ensure that all generated queries adhere to this schema and constraints.

    ### Database Schema:
    ### Database Schema:

    #### Table: `Securities`
    - **Description**: Stores information about securities (e.g., stocks, bonds).
    - **Columns**:
      - `Securities_Code` (VARCHAR(20), PRIMARY KEY): Unique identifier for each security.
      - `sec_englishname` (VARCHAR(100)): English name of the security.
      - `ipo_date` (DATE): The initial public offering date.
      - `exch_eng` (VARCHAR(10)): Exchange code where the security is listed (e.g., NYSE).
      - `country` (VARCHAR(10)): Country code for the security.

    #### Table: `Companies`
    - **Description**: Contains company-level information.
    - **Columns**:
      - `Company_code` (VARCHAR(10), PRIMARY KEY): Unique company identifier.
      - `Securities_Code` (VARCHAR(20)): Foreign key referencing `Securities(Securities_Code)`.
      - `comp_name_eng` (VARCHAR(255)): English name of the company.
      - `phone` (TEXT): Contact phone numbers for the company.
      - `industry_swcode_2021` (BIGINT): Industry classification code.
      - `founddate1` (DATE): Establishment date of the company.
      - `regcapital` (DECIMAL(15,4)): Registered capital of the company.
      - `employee_number` (INT): Number of employees.

    #### Table: `balance_sheet`
    - **Description**: Stores balance sheet information for companies.
    - **Columns**:
      - `balanceCode` (VARCHAR(10), PRIMARY KEY): Unique identifier for each balance sheet.
      - `windcode` (VARCHAR(20)): Foreign key referencing `Securities(Securities_Code)`.
      - `tot_assets` (DECIMAL(15,4)): Total assets of the company.
      - `tot_cur_assets` (DECIMAL(15,4)): Current assets of the company.
      - `inventories` (DECIMAL(15,4)): Inventory value.
      - `fix_assets` (DECIMAL(15,4)): Fixed assets value.
      - `tot_liab` (DECIMAL(15,4)): Total liabilities of the company.
      - `tot_non_cur_liab` (DECIMAL(15,4)): Non-current liabilities.
      - `tot_cur_liab` (DECIMAL(15,4)): Current liabilities.
      - `eqy_belongto_parcomsh` (DECIMAL(15,4)): Equity attributable to parent company shareholders.

    #### Table: `income_statement`
    - **Description**: Contains income statement data for companies.
    - **Columns**:
      - `IncomeCode` (VARCHAR(10), PRIMARY KEY): Unique identifier for each income statement.
      - `BalanceCode` (VARCHAR(10)): Foreign key referencing `balance_sheet(balanceCode)`.
      - `tot_oper_rev` (DECIMAL(15,4)): Total operating revenue.
      - `tot_oper_cost` (DECIMAL(15,4)): Total operating costs.
      - `opprofit` (DECIMAL(15,4)): Operating profit.
      - `tot_profit` (DECIMAL(15,4)): Total profit.
      - `tax` (DECIMAL(15,4)): Taxes paid.
      - `net_profit_is` (DECIMAL(15,4)): Net profit.
      - `tot_compreh_inc_parent_comp` (DECIMAL(15,4)): Comprehensive income attributable to the parent company.
      - `selling_dist_exp` (DECIMAL(15,4)): Selling expenses.
      - `gerl_admin_exp` (DECIMAL(15,4)): General and administrative expenses.
      - `rd_exp` (DECIMAL(15,4)): R&D expenses.
      - `fin_exp_is` (DECIMAL(15,4)): Financial expenses.

    #### Table: `financial_analysis`
    - **Description**: Contains financial analysis metrics for companies.
    - **Columns**:
      - `FAID` (VARCHAR(10), PRIMARY KEY): Unique identifier for financial analysis data.
      - `BalanceCode` (VARCHAR(10)): Foreign key referencing `balance_sheet(balanceCode)`.
      - `eps_basic` (DECIMAL(15,4)): Basic earnings per share.
      - `roe_basic` (DECIMAL(15,4)): Return on equity (basic).
      - `profittogr` (DECIMAL(15,4)): Total profit growth rate.
      - `currentRatio` (DECIMAL(15,4)): Current ratio.
      - `quick` (DECIMAL(15,4)): Quick ratio.
      - `fa_debttoeqy` (DECIMAL(15,4)): Financial leverage (debt-to-equity ratio).
      - `invturndays` (DECIMAL(15,4)): Inventory turnover days.
      - `invturn` (DECIMAL(15,4)): Inventory turnover rate.
      - `turnover_ttm` (DECIMAL(15,4)): Turnover (TTM).
      - `yoy_tr` (DECIMAL(15,4)): Year-over-year operating revenue growth rate.
      - `yoyprofit` (DECIMAL(15,4)): Year-over-year profit growth rate.

    #### Table: `esg`
    - **Description**: Stores ESG (Environmental, Social, Governance) data for companies.
    - **Columns**:
      - `ESG_reportID` (VARCHAR(10), PRIMARY KEY): Unique identifier for ESG report.
      - `Company_code` (VARCHAR(10)): Foreign key referencing `Companies(Company_code)`.
      - `esg_rating_wind` (VARCHAR(10)): ESG rating (e.g., AA, BBB).
      - `esg_escore_wind` (DECIMAL(10,2)): ESG environment score.
      - `esg_sscore_wind` (DECIMAL(10,2)): ESG social score.
      - `esg_gscore_wind` (DECIMAL(10,2)): ESG governance score.
      - `esg_rating_ftserussell` (DECIMAL(10,2)): FTSE Russell ESG rating.
      - `esg_mgmtscore_wind2` (DECIMAL(10,3)): ESG management score.
      - `esg_eventscore_wind2` (DECIMAL(10,3)): ESG event score.


    ### Rules for Query Generation:
    1. Only use the tables and columns defined in the schema.
    2. Ensure foreign key relationships are respected (e.g., `Company_code` in `esg` must exist in `Companies`).
    3. Avoid creating new tables, columns, or values not present in the schema.
    4. If performing joins, ensure that foreign key relationships are used correctly.
    You only need to generate the sql code 
    """
def index(request):
    """Render the front-end HTML page."""
    return render(request, "queryapp/index.html")

client = OpenAI(
    api_key="YourApiKey"  # Replace with your OpenAI API key
)


def execute_sql_query(query):
    """Execute SQL query and fetch results."""
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return columns, rows


def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if you prefer
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


@csrf_exempt
def natural_language_query(request):
    if request.method == "POST":
        try:
            # Parse the JSON request body
            data = json.loads(request.body.decode("utf-8"))
            natural_language_query = data.get("query", "")

            if not natural_language_query:
                return JsonResponse({"error": "Query field is required"}, status=400)

            # Call the chat_gpt function
            raw_sql_query = chat_gpt(prompt +
                f"Translate this natural language query into SQL: {natural_language_query}")
            
            # Strip backticks if they exist
            sql_query = raw_sql_query.strip("`")
            sql_query = sql_query.strip("sql")
            # Execute the SQL query and fetch results
            try:
                columns, rows = execute_sql_query(sql_query)

                # Combine columns and rows into a structured table
                table_data = [dict(zip(columns, row)) for row in rows]

            except Exception as e:
                return JsonResponse({"error": f"Error executing SQL query: {str(e)}", "sql": sql_query})

            return JsonResponse({
                "query": natural_language_query,
                "sql": sql_query,
                "table": table_data  # Structured table data
            })

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)