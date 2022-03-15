from fastapi import Depends, HTTPException, Response, status, APIRouter
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import oauth2, schemas
from app.database import get_db
from app.models import CarryForward, ExpenseTable, IncomeTable
from app.utils import RoleChecker

allow = RoleChecker(["admin"])

router = APIRouter(
    prefix="/table",
    tags=["Tables"]
)


@router.get("/{createdAt}")
async def get_table(createdAt: str, db: Session = Depends(get_db), curr_user: UUID4 = Depends(oauth2.get_current_user)):
    # sourcery skip: inline-immediately-returned-variable
    incomeTable = db.query(IncomeTable).filter(
        IncomeTable.createdAt == createdAt).order_by(IncomeTable.date).all()
    expenseTable = db.query(ExpenseTable).filter(
        ExpenseTable.createdAt == createdAt).order_by(ExpenseTable.expenseDate).all()
    cfQuery = db.query(CarryForward).filter(
        CarryForward.createdAt == createdAt)
    cfData = cfQuery.first()
    return {"income": incomeTable, "expense": expenseTable, "cf": cfData}


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow)])
async def create_table(table: schemas.Table, db: Session = Depends(get_db),):
    # sourcery skip: inline-immediately-returned-variable
    tableDict = table.dict()
    incomeTableData = tableDict["income"]
    expenseTableData = tableDict["expense"]
    cfTableData = tableDict["total"]
    print(cfTableData)

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

    cfTableQuery = db.query(CarryForward).filter(
        CarryForward.createdAt == tableDict["createdAt"])
    cfTableEntry = cfTableQuery.first()
    if cfTableEntry is not None:
        cfTableQuery.update(cfTableData)
    else:
        cfTableData["createdAt"] = tableDict["createdAt"]
        newCFtbl = CarryForward(**cfTableData)
        db.add(newCFtbl)

    db.commit()

    newIncomeTables = db.query(IncomeTable).filter(
        IncomeTable.createdAt == tableDict["createdAt"]).all()

    newExpenseTables = db.query(ExpenseTable).filter(
        ExpenseTable.createdAt == tableDict["createdAt"]).all()

    newCFTables = db.query(CarryForward).filter(
        CarryForward.createdAt == tableDict["createdAt"]).first()

    return {"income": newIncomeTables, "expense": newExpenseTables, "total": newCFTables}


@router.delete("/", dependencies=[Depends(allow)])
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
