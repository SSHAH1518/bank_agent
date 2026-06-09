from pathlib import Path

import pandas as pd
import json
from fastapi import UploadFile
from fastapi import File
from fastapi import APIRouter

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_serrvice import chunk_text_by_lines
from app.agents.extraction_agent import extract_bank_data as extract_bank_details
from app.services.categorization_service import (
    categorize_transaction
)
from app.services.analytics_service import category_summary
from app.agents.advisor import generate_financial_advice


MAX_FILE_SIZE = 10 * 1024 * 1024

UPLOAD_DIR = "app/documents"

Path(UPLOAD_DIR).mkdir(exist_ok=True)

router = APIRouter()


def _json_safe(value):
    if isinstance(value, pd.Period):
        return str(value)

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if isinstance(value, pd.Timedelta):
        return str(value)

    if isinstance(value, dict):
        return {
            str(key): _json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]

    if hasattr(value, "tolist"):
        try:
            return value.tolist()
        except Exception:
            pass

    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            pass

    return value


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        return {
            "error": "File exceeds 10MB limit"
        }

    with open(file_path, "wb") as f:
        f.write(content)

    text = extract_text_from_pdf(file_path)

    chunks = chunk_text_by_lines(
        text,
        rows_per_chunk=50
    )

    account_holder = None
    account_number = None

    all_transactions = []

    for index, chunk in enumerate(chunks):

        print(
            f"Processing chunk {index + 1}"
        )

        result = extract_bank_details(
            chunk
        )

        if not account_holder:
            account_holder = result.get(
                "account_holder"
            )

        if not account_number:
            account_number = result.get(
                "account_number"
            )

        all_transactions.extend(
            result.get(
                "transactions",
                []
            )
        )

    if not all_transactions:
        return {
            "error": "No transactions found"
        }

    df = pd.DataFrame(
        all_transactions
    )
    df = df.dropna(subset=["date"])

    df["category"] = (
        df["description"]
        .fillna("")
        .apply(categorize_transaction)
    )

    category_breakdown = category_summary(df)

    print("\n===== DATAFRAME =====")
    print(df.head())
    print(df.shape)
    print("=====================\n")

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )
    print("\n===== SUMMARY =====")

    print(
        "Account Holder:",
        account_holder
    )

    print(
        "Account Number:",
        account_number
    )

    print(
        "Total Credit:",
        df[df["type"].str.lower() == "credit"]["amount"].sum()
    )

    print(
        "Total Debit:",
        df[df["type"].str.lower() == "debit"]["amount"].sum()
    )

    print("===================\n")

    df["type"] = (
        df["type"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    total_credit = (
        df[
            df["type"] == "credit"
        ]["amount"]
        .sum()
    )

    total_debit = (
        df[
            df["type"] == "debit"
        ]["amount"]
        .sum()
    )

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    monthly_summary_data = (
        df.groupby(df["date"].dt.to_period("M"))
        ["amount"]
        .sum()
        .reset_index()
    )

    monthly_summary_data["date"] = (
        monthly_summary_data["date"]
        .astype(str)
    )
    monthly_summary_data["amount"] = (
        monthly_summary_data["amount"]
        .astype(float)
    )
        
    def top_transactions(df):

        records = (
            df.sort_values(
                by="amount",
                ascending=False
            )
            .head(10)
            .copy()
        )

        records["amount"] = records["amount"].astype(float)
        records["date"] = pd.to_datetime(
            records["date"],
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        return records.to_dict("records")

    df["month"] = pd.to_datetime(
        df["date"]
    ).dt.to_period("M")

    df["is_credit"] = (
        df["type"] == "credit"
    )

    df["is_debit"] = (
        df["type"] == "debit"
    )

    csv_path = (
        file_path
        .replace(".pdf", ".csv")
    )

    df_to_save = df.copy()

    df_to_save["month"] = (
        df_to_save["month"]
        .astype(str)
    )

    df_to_save.to_csv(
        csv_path,
        index=False
    )

    print(
        f"\nSaved CSV: {csv_path}\n"
    )

    category_breakdown = (
        df.groupby("category")["amount"]
        .sum()
        .to_dict()
    )

    net_cashflow = total_credit - total_debit

    analytics = _json_safe({
        "account_holder": account_holder,
        "account_number": account_number,
        "total_credit": float(total_credit),
        "total_debit": float(total_debit),
        "net_cashflow": float(net_cashflow),

        "monthly_summary": monthly_summary_data.to_dict("records"),

        "category_breakdown": {
            str(k): float(v)
            for k, v in category_breakdown.items()
        },

        "top_transactions": top_transactions(df)
    })

    analytics_path = (
        file_path
        .replace(".pdf", "_analytics.json")
    )

    with open(
        analytics_path,
        "w"
    ) as f:
        json.dump(
            analytics,
            f,
            indent=4
        )

    print(
        f"Saved analytics: {analytics_path}"
    )
    advice = generate_financial_advice(analytics)

    print("\n===== ADVICE =====")
    print(advice)
    print("==================\n")

    return {
        "analytics": analytics,
        "advice": advice
    }