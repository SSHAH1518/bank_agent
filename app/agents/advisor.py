import json
import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

def convert_numpy(obj):

    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    if isinstance(obj, (pd.Period, pd.Timestamp, pd.Timedelta)):
        return str(obj)

    if hasattr(obj, "tolist"):
        try:
            return obj.tolist()
        except Exception:
            pass

    if hasattr(obj, "item"):
        try:
            return obj.item()
        except Exception:
            pass

    return str(obj)

def generate_financial_advice(analytics):

    prompt = f"""
You are a financial analyst.

Your job is to analyze transaction data and provide evidence-based observations.

Financial Data:

{json.dumps(analytics, indent=2, default=convert_numpy)}

========================================
CATEGORY DEFINITIONS
========================================

Salary:
Income from employment.

Investments:
SIPs, Mutual Funds,
Index Funds, ETFs,
Stocks, Bonds.

Savings:
Savings transfers,
Fixed Deposits,
Recurring Deposits,
Emergency Funds.

Dining:
Restaurants,
Food Delivery,
Cafes.

Luxury Spending:
Designer Brands,
Premium Shopping,
Luxury Goods.

Travel:
Flights,
Hotels,
Vacations.

Medical Expenses:
Hospitals,
Clinics,
Pharmacies.

Utilities:
Electricity,
Water,
Internet,
Gas.

Credit Card Payment:
Repayment of debt.
This is NOT spending.

========================================
INTERPRETATION RULES
========================================

Salary is income.

Savings are positive behavior.

Investments are positive behavior.

Credit card payments are debt repayment.

Transfers between personal accounts
are not expenses.

Do NOT classify investments
as risky simply because
the amount is large.

Do NOT classify savings
as spending.

Do NOT classify salary
as spending.

Large amounts alone
do not indicate risk.

========================================
RISK DETECTION RULES
========================================

Only report a risk if
there is direct evidence.

Valid examples:

- Very high luxury spending
relative to total outflow

- Very high dining spending
relative to total outflow

- Large ATM withdrawals

- Very low savings
despite high income

- Extremely concentrated spending
in a discretionary category

Invalid examples:

- High rent

- High investments

- High savings

- High salary

- Missing categories

- Lack of data

Never create a risk from:

- missing information
- absent categories
- insufficient evidence

If evidence does not exist,
omit the risk entirely.

Use the provided ratios when
evaluating spending patterns.

========================================
RECOMMENDATION RULES
========================================

Every recommendation must be linked
to a specific observation or risk.

Do NOT provide generic advice.

BAD:
"Create a budget."

GOOD:
"Dining expenses represent 28% of all outflows. Consider reducing restaurant spending."

BAD:
"Diversify investments."

GOOD:
"95% of investment activity appears concentrated in SIP contributions."

If there is no evidence,
do not create a recommendation.

========================================
OUTPUT REQUIREMENTS
========================================

For spending habits:

Describe only the most significant categories.

For risks:

Provide:

- risk
- evidence
- category
- amount
- explanation

Only include risks supported
by data.

For recommendations:

Each recommendation must reference
a specific spending pattern
or risk.

Return ONLY valid JSON.

Format:

{{
  "summary": "",
  "spending_habits": [],
  "risks": [],
  "recommendations": []
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content