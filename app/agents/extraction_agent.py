from groq import Groq
from app.schemas.bank_statement import (BankStatement)
import os
import json
from dotenv import load_dotenv
from  app.schemas.bank_statement import BankStatement
import re

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_bank_details(chunk:str):
    prompt = f"""
    You are a financial data extraction system.

    Analyze the bank statement data.

    Return ONLY valid JSON.

    Rules:
    1. Return valid JSON only.
    2. No markdown.
    3. No explanations.
    4. No code fences.
    5. Every value must be a final number.
    6. Never return calculations like:
    1000 + 2000
    7. Calculate totals yourself.
    8. All amounts must be floats.

    Schema:

    {{
    "monthly_summary": [
        {{
        "month": "YYYY-MM",
        "money_received": 0.0,
        "money_spent": 0.0,
        "net_cashflow": 0.0
        }}
    ]
    }}

    Bank Data:

    {chunk}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role":"user", 
                "content":prompt
            }
        ]
    )

    result = response.choices[0].message.content

    data = json.loads(result)

    print("===== MODEL RESPONSE =====")
    print(result)
    print("==========================") 


    return data