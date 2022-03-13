from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.models import ExpenseTable, IncomeTable

router = APIRouter(
    prefix="/table",
    tags=["Tables"]
)


@router.get("/{createdAt}")
async def get_table(createdAt: str, db: Session = Depends(get_db)):
    # sourcery skip: inline-immediately-returned-variable
    incomeTable = db.query(IncomeTable).filter(
        IncomeTable.createdAt == createdAt).all()
    expenseTable = db.query(ExpenseTable).filter(
        ExpenseTable.createdAt == createdAt).all()
    return {"income": incomeTable, "expense": expenseTable}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_table(table: schemas.Table, db: Session = Depends(get_db)):
    # sourcery skip: inline-immediately-returned-variable
    tableDict = table.dict()
    incomeTableData = tableDict["income"]
    expenseTableData = tableDict["expense"]

    for value in incomeTableData:
        value["createdAt"] = tableDict["createdAt"]
        if value['id'] is not None:
            post_query = db.query(IncomeTable).filter(
                IncomeTable.id == value["id"])
            post_query.update(value)
        else:
            newIncomeTbl = IncomeTable(**value)
            db.add(newIncomeTbl)

    for value in expenseTableData:
        value["createdAt"] = tableDict["createdAt"]
        if value["id"] is not None:
            expense_query = db.query(ExpenseTable).filter(
                ExpenseTable.id == value["id"])
            expense_query.update(value)
        else:
            newExpenseTbl = ExpenseTable(**value)
            db.add(newExpenseTbl)

    db.commit()

    newIncomeTables = db.query(IncomeTable).filter(
        IncomeTable.createdAt == tableDict["createdAt"]).all()

    newExpenseTables = db.query(ExpenseTable).filter(
        ExpenseTable.createdAt == tableDict["createdAt"]).all()

    return {"income": newIncomeTables, "expense": newExpenseTables}


@router.delete("/")
async def delete_entries(ids: schemas.EntriesToDelete, db: Session = Depends(get_db)):
    for value in ids.incomeToDelete:
        deleteQuery = db.query(IncomeTable).filter(IncomeTable.id == value)
        deleteEntry = deleteQuery.first()
        if deleteEntry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Entry with id: {value} Doesnt Exist")
        deleteQuery.delete()

    for value in ids.expenseToDelete:
        deleteQuery = db.query(ExpenseTable).filter(ExpenseTable.id == value)
        deleteEntry = deleteQuery.first()
        if deleteEntry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Entry with id: {value} Doesnt Exist")
        deleteQuery.delete()

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
