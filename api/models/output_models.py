from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI

class Payment_Information(BaseModel):
    """Relevant information extracted from payment schedules"""

    bank: str = Field(description="The Bank that issued the loan")
    monthly_payment: str = Field(description="The monthly payment amount the user pays for their loan.")
    total_loan_amount: str = Field(description="The total amount loaned by the bank.")
    interest_rate: str = Field(description="Find the interest rate at which the loan was issued.")

class Salary_Information(BaseModel):
    """Relevant information extracted from salary slips"""

    company: str = Field(description="The employer or entity that issued the payroll slip.")
    net_salary: str = Field(description="The net salary that the employee receives.")
    variable_amounts: str = Field(description="All variable amounts listed in the payroll slip.")

payment_functions = [convert_pydantic_to_openai_function(Payment_Information)]
salary_functions = [convert_pydantic_to_openai_function(Salary_Information)]