from asyncio.windows_events import NULL
from typing import Optional
from pydantic import BaseModel


class Income(BaseModel):
    id: int
    name: str
    flatNo: int
    amount: int
    createdAt: str


class Expense(BaseModel):
    id: int
    expenseName: str
    vrNo: Optional[int] = NULL
    expenseDate: str
    expenseReason: Optional[str] = ""
    createdAt: str
