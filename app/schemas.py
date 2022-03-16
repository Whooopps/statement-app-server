
from datetime import datetime
from typing import List, Optional
from pydantic import UUID4, BaseModel, EmailStr


class IncomeTable(BaseModel):
    name: Optional[str] = None
    flatNo: Optional[int] = None
    amount: Optional[int] = None
    date: Optional[str] = None
    id: Optional[int] = None


class ExpenseTable(BaseModel):
    expenseName: Optional[str] = None
    vrNo: Optional[int] = None
    expenseDate: Optional[str] = None
    expenseReason: Optional[str] = None
    expenseAmount: Optional[int] = None
    id: Optional[int] = None


class CF(BaseModel):
    cf: Optional[int] = None
    nextMonthCF: Optional[int] = None


class Table(BaseModel):
    income: Optional[List[IncomeTable]] = None
    expense: Optional[List[ExpenseTable]] = None
    cf: CF
    createdAt: str


class EntriesToDelete(BaseModel):
    income: List[int]
    expense: List[int]


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    id: Optional[UUID4] = None
    expires: Optional[datetime]


class UserOut(BaseModel):
    id: UUID4
    email: EmailStr
    userCreatedAt: datetime

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class CheckEmail(BaseModel):
    email: EmailStr
