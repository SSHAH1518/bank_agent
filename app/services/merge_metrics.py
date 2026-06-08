def merge_monthly_metrics(chunk_results):
    merged = {}

    for result in chunk_results:
        for month_data in result["monthly_summary"]:
            month = month_data["month"]

            if month not in merged:
                merged[month] = {
                    "credited": 0,
                    "debited": 0
                }   

            merged[month]["credited"] += (
                month_data.get("credited", 0)
            )

            merged[month]["debited"] += (
                month_data.get("debited", 0)
            )

    return merged
