
from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr


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


class CF(BaseModel):
    cf: Optional[int] = 0
    nextMonthCF: Optional[int] = 0


class Table(BaseModel):
    income: Optional[List[IncomeTable]] = None
    expense: Optional[List[ExpenseTable]] = None
    total: CF
    createdAt: str


class EntriesToDelete(BaseModel):
    incomeToDelete: Optional[List[int]] = None
    expenseToDelete: Optional[List[int]] = None


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    id: Optional[UUID4] = None


class UserOut(BaseModel):
    id: UUID4
    email: EmailStr
    userCreatedAt: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
