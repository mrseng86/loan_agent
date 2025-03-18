

from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI(title="贷款计算AI Agent")

# 允许跨域请求
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    principal: float  # 贷款金额
    monthly_interest_rate: float  # 月利率（%）
    loan_months: int  # 贷款期数（月）
    service_fee: float = 10  # 固定服务费（默认 10）
    commission_rate: float = 18  # 佣金比率（默认 18%）

def round_up_to_nearest_ten(value):
    """ 进位到最近的 10 的倍数 """
    return math.ceil(value / 10) * 10

def calculate_custom_monthly_payment(principal, monthly_interest_rate, loan_months, service_fee, commission_rate):
    """ 计算贷款的每月还款金额 """
    # 计算本金加上佣金
    principal_with_commission = principal * (1 + commission_rate / 100)

    # 计算总利息
    total_interest = principal_with_commission * (monthly_interest_rate / 100) * loan_months

    # 计算总还款额
    total_repayment = principal_with_commission + total_interest

    # 计算每月还款
    monthly_payment = total_repayment / loan_months

    # 加上服务费
    monthly_payment += service_fee

    # 进位到最近的 10
    monthly_payment = round_up_to_nearest_ten(monthly_payment)

    return monthly_payment

@app.post("/calculate_custom_payment")
async def calculate_payment(data: LoanRequest):
    """ 计算还款金额 API """
    monthly_payment = calculate_custom_monthly_payment(
        data.principal, data.monthly_interest_rate, data.loan_months, data.service_fee, data.commission_rate
    )
    return {"monthly_payment": monthly_payment}

