def categorize_transaction(description):

    desc = description.lower()

    if "upi" in desc:
        return "UPI Payment"

    if "salary" in desc:
        return "Salary"

    if "atm" in desc:
        return "ATM Withdrawal"

    if "neft" in desc:
        return "Bank Transfer"

    if "rtgs" in desc:
        return "Bank Transfer"

    if "imps" in desc:
        return "Bank Transfer"

    if "fuel" in desc:
        return "Fuel"

    if "rent" in desc:
        return "Rent"

    if "insurance" in desc:
        return "Insurance"

    return "Other"