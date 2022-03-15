from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from .database import Base


class IncomeTable(Base):
    __tablename__ = "incomeTable"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    flatNo = Column(Integer)
    amount = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    createdAt = Column(String, nullable=False)
    entryAdded = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
                        )


class ExpenseTable(Base):
    __tablename__ = "expenseTable"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    expenseName = Column(String, nullable=False)
    vrNo = Column(Integer)
    expenseAmount = Column(Integer, nullable=False)
    expenseDate = Column(String, nullable=False)
    expenseReason = Column(String)
    createdAt = Column(String, nullable=False)
    entryAdded = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
                        )


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="guest")
    userCreatedAt = Column(TIMESTAMP(timezone=True),
                           nullable=False, server_default=text("now()"))


class CarryForward(Base):
    __tablename__ = "carryforward"
    createdAt = Column(String, primary_key=True, index=True, nullable=False)
    cf = Column(Integer, nullable=False, default=0)
    nextMonthCF = Column(Integer, nullable=False, default=0)
