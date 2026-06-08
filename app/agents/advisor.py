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
You are a financial advisor.

Analyze this financial summary:

{json.dumps(analytics, indent=2, default=convert_numpy)}

Provide:

1. Spending habits
2. Savings habits
3. Financial risks
4. Recommendations

Return JSON:

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