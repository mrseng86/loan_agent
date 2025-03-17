

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import math
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="贷款计算AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    principal: float
    monthly_interest_rate: float
    loan_months: int
    service_fee: float = 10
    commission_rate: float = 15

# 正确的自定义贷款计算公式
def calculate_custom_monthly_payment(principal, monthly_interest_rate, loan_months, service_fee, commission_rate):
    principal_with_commission = principal * (1 + commission_rate / 100)
    monthly_interest = principal_with_commission * (monthly_interest_rate / 100)
    total_interest = monthly_interest * loan_months
    total_repayment = principal_with_commission + total_interest
    monthly_payment = total_repayment / loan_months + service_fee
    monthly_payment = math.ceil(monthly_payment / 10) * 10 if monthly_payment % 10 > 5 else round(monthly_payment / 10) * 10
    return monthly_payment

# 生成正确的还款计划表
def generate_custom_repayment_schedule(principal, monthly_interest_rate, loan_months, service_fee, commission_rate):
    principal_with_commission = principal * (1 + commission_rate / 100)
    monthly_interest = principal_with_commission * (monthly_interest_rate / 100)
    total_interest = monthly_interest * loan_months
    total_repayment = principal_with_commission + total_interest
    monthly_payment = total_repayment / loan_months + service_fee
    monthly_payment = math.ceil(monthly_payment / 10) * 10 if monthly_payment % 10 > 5 else round(monthly_payment / 10) * 10

    schedule = []
    remaining_balance = total_repayment

    for month in range(1, loan_months + 1):
        interest = monthly_interest
        principal_paid = monthly_payment - service_fee - interest
        remaining_balance -= principal_paid
        schedule.append({
            "Month": month,
            "Monthly Payment": round(monthly_payment, 2),
            "Interest": round(interest, 2),
            "Principal": round(principal_paid, 2),
            "Service Fee": service_fee,
            "Remaining Balance": round(max(remaining_balance, 0), 2)
        })

    return pd.DataFrame(schedule)

@app.post("/calculate_custom_payment")
def calculate_payment(loan: LoanRequest):
    monthly_payment = calculate_custom_monthly_payment(
        loan.principal, loan.monthly_interest_rate, loan.loan_months, loan.service_fee, loan.commission_rate
    )
    return {"monthly_payment": monthly_payment}

@app.post("/custom_repayment_schedule")
def custom_repayment_schedule(loan: LoanRequest):
    schedule_df = generate_custom_repayment_schedule(
        loan.principal, loan.monthly_interest_rate, loan.loan_months, loan.service_fee, loan.commission_rate
    )
    return schedule_df.to_dict(orient='records')