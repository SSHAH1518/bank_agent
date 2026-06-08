def categorize_transaction(description):

    desc = description.lower()

    if "upi" in desc or "qr" in desc or "paytm" in desc or "phonepe" in desc or "google pay" in desc:
        return "UPI Payment"

    if "salary" in desc or "monthly income" in desc or "payroll" in desc:
        return "Salary"

    if "atm" in desc or "cash withdrawal" in desc or "withdrawal" in desc:
        return "ATM Withdrawal"

    if "neft" in desc or "rtgs" in desc or "imps" in desc or "bank transfer" in desc or "fund transfer" in desc:
        return "Bank Transfer"

    if "fuel" in desc or "petrol" in desc or "diesel" in desc or "gas station" in desc:
        return "Fuel"

    if "rent" in desc or "house rent" in desc or "monthly rent" in desc:
        return "Rent"

    if "insurance" in desc or "premium" in desc:
        return "Insurance"

    if "sip" in desc or "mutual fund" in desc or "index fund" in desc or "invest" in desc or "mf" in desc:
        return "Investments"

    if "dividend" in desc or "interest income" in desc:
        return "Dividend Income"

    if "emergency fund" in desc or "savings" in desc or "fixed deposit" in desc or "fd" in desc:
        return "Emergency Savings"

    if "groceries" in desc or "mart" in desc or "supermarket" in desc or "grocery" in desc:
        return "Groceries"

    if "dining" in desc or "restaurant" in desc or "cafe" in desc or "food" in desc:
        return "Dining"

    if "travel" in desc or "trip" in desc or "hotel" in desc or "flight" in desc or "train" in desc:
        return "Travel"

    if "gadget" in desc or "mobile" in desc or "laptop" in desc or "electronics" in desc or "luxury" in desc:
        return "Luxury Spending"

    if "credit card" in desc or "cc bill" in desc or "card payment" in desc:
        return "Credit Card Payment"

    if "shopping" in desc or "fashion" in desc or "amazon" in desc or "flipkart" in desc:
        return "Shopping"

    if "health" in desc or "pharmacy" in desc or "clinic" in desc or "hospital" in desc:
        return "Healthcare"

    if "education" in desc or "tuition" in desc or "course" in desc or "college" in desc:
        return "Education"

    if "overdraft" in desc or "bank charges" in desc or "service charge" in desc or "processing fee" in desc or "ledger fee" in desc:
        return "Bank Charges"

    if "subscription" in desc or "netflix" in desc or "spotify" in desc or "membership" in desc:
        return "Subscriptions"

    return "Other"