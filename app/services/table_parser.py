import pandas as pd


def build_dataframe(all_transactions):

    rows = []

    for chunk in all_transactions:

        rows.extend(
            chunk["transactions"]
        )

    return pd.DataFrame(rows)