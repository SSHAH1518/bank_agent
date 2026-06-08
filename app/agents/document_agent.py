import os
import json

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def understand_statement(text: str):

    prompt = f"""
    Extract transactions from this bank statement.

    Return ONLY valid JSON.

    Do NOT:

    - Explain
    - Write Python code
    - Use markdown
    - Use ```json

    Return exactly:

    {{
        "account_holder": "",
        "account_number": "",
        "transactions": [
            {{
                "date": "",
                "description": "",
                "type": "",
                "amount": 0
            }}
        ]
    }}

    Bank Statement:

    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": """
                You are a JSON extraction engine.

                Return ONLY valid JSON.

                Never explain.
                Never generate Python code.
                Never generate markdown.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    return json.loads(
        result.replace("```json", "")
              .replace("```", "")
    )