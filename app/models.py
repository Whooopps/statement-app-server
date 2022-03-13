from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from .database import Base


class IncomeTable(Base):
    __tablename__ = "incomeTable"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    flatNo = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    createdAt = Column(String, nullable=False)
    entryAdded = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')
                        )
