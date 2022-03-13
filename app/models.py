from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from .database import Base


class IncomeTable(Base):
    __tablename__ = "incomeTable"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    flatNo = Column(Integer, nullable=False)
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
    expenseDate = Column(String, nullable=False)
    expenseReason = Column(String)
    createdAt = Column(String, nullable=False)
    entryAdded = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
                        )
