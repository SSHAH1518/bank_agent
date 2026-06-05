from pydantic import BaseModel

class MonthlySummary(BaseModel):
    month: str
    money_received: float
    money_spent: float
    net_cashflow: float

class BankStatement(BaseModel):
    monthly_summary: list[MonthlySummary]