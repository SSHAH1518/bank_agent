import pandas as pd

def category_summary(df):

    debit_df = df[df["type"] == "Debit"]

    summary = (
        debit_df
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .to_dict()
    )

    return summary