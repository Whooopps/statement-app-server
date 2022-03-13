
from ast import Str
from typing import List, Optional
from pydantic import BaseModel

# API RESPONSE

# USER RESPONSE


class IncomeTable(BaseModel):
    name: str
    flatNo: int
    amount: int
    date: str
    id: Optional[int] = None


class ExpenseTable(BaseModel):
    expenseName: str
    vrNo: Optional[int] = None
    expenseDate: str
    expenseReason: Optional[str] = ""
    id: Optional[int] = None


class Table(BaseModel):
    income: List[IncomeTable]
    expense: List[ExpenseTable]
    createdAt: str


class EntriesToDelete(BaseModel):
    incomeToDelete: List[int]
    expenseToDelete: List[int]
