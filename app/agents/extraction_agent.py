import os
import json
import re
import time

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def parse_llm_response(response_text: str):
    """
    Extract valid JSON from LLM response.
    """

    try:
        return json.loads(response_text)

    except Exception:

        print("Direct JSON parsing failed.")

        # Remove markdown fences if present

        cleaned = response_text.replace("```json", "")
        cleaned = cleaned.replace("```", "").strip()

        # Find first JSON object

        match = re.search(
            r"\{.*\}",
            cleaned,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                f"No JSON found in response:\n{response_text[:500]}"
            )

        json_text = match.group(0)

        return json.loads(json_text)


def extract_bank_data(chunk: str):

    prompt = f"""
Extract transactions from this bank statement.

Return ONLY valid JSON.

DO NOT:
- Explain anything
- Generate Python code
- Use markdown
- Use triple backticks

Return EXACTLY this schema:

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

Rules:

1. Extract every transaction.
2. Amount must be numeric.
3. Type must be Credit or Debit.
4. Description should contain the payment narration.
5. Missing account holder/account number is allowed.
6. Return JSON only.

Bank Statement:

{chunk}
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a JSON extraction engine.

Return ONLY valid JSON.

Never explain.
Never generate code.
Never generate markdown.
Never generate text before JSON.
Never generate text after JSON.
"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                response_format={
                    "type": "json_object"
                }
            )

            result = response.choices[0].message.content

            print("\n===== RAW RESPONSE =====")
            print(result[:2000])
            print("========================\n")

            parsed = parse_llm_response(result)

            return parsed

        except Exception as e:

            print(
                f"Attempt {attempt + 1}/{max_retries} failed:"
            )
            print(e)

            if attempt < max_retries - 1:
                time.sleep(2)

    print("LLM extraction failed.")

    return {
        "account_holder": "",
        "account_number": "",
        "transactions": []
    }