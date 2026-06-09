CATEGORY_KEYWORDS = {
    "UPI Payment": ["upi", "qr", "paytm", "phonepe", "google pay"],
    "Salary": ["salary", "monthly income", "payroll"],
    "ATM Withdrawal": ["atm", "cash withdrawal", "withdrawal"],
    "Bank Transfer": ["neft", "rtgs", "imps", "bank transfer"],
    "Fuel": ["fuel", "petrol", "diesel", "gas station"],
    "Rent": ["rent", "house rent", "monthly rent"],
    "Insurance": ["insurance", "premium"],
    "Investments": [
        "sip", "mutual fund", "etf", "index fund", "stock purchase", "equity",
        "shares", "nifty", "sensex", "zerodha", "groww", "upstox",
        "angel one", "brokerage", "investment"
    ],
    "Dividend Income": ["dividend", "interest income"],
    "Savings": ["savings transfer", "transfer to savings", "emergency fund transfer", "recurring deposit", "fixed deposit", "fd"],
    "Groceries": ["groceries", "mart", "supermarket", "grocery"],
    "Dining": ["dining", "restaurant", "cafe", "food"],
    "Travel": ["travel", "trip", "hotel", "flight", "train"],
    "Luxury Spending": ["gadget", "laptop", "electronics", "luxury"],
    "Credit Card Payment": ["credit card", "cc bill", "card payment"],
    "Shopping": ["shopping", "fashion", "amazon", "flipkart"],
    "Medical Expenses": ["hospital", "doctor", "clinic", "medical", "medicine", "pharmacy", "healthcare", "apollo", "fortis"],
    "Utilities": ["electricity bill", "water bill", "gas bill", "internet", "broadband", "wifi", "mobile recharge", "utility payment"],
    "Education": ["education", "tuition", "course", "college"],
    "Bank Charges": ["overdraft", "bank charges", "service charge", "processing fee", "ledger fee"],
    "Subscriptions": ["subscription", "netflix", "spotify", "membership"],
}


def categorize_transaction(description):
    desc = (description or "").lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in desc for keyword in keywords):
            return category

    return "Unclassified"