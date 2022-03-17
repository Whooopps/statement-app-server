from io import BytesIO
from fastapi import Depends, HTTPException, Response, status, APIRouter
from fastapi.responses import StreamingResponse
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import oauth2, schemas
from app.database import get_db
from app.models import CarryForward, ExpenseTable, IncomeTable
from app.utils import RoleChecker
import xlsxwriter
import calendar
allow = RoleChecker(["admin"])

router = APIRouter(
    prefix="/table",
    tags=["Tables"]
)


@router.get("/xlsx/{createdAt}")
async def table(createdAt: str, db: Session = Depends(get_db)):

    splitCreatedAt = createdAt.split("-")
    monthName = calendar.month_abbr[int(splitCreatedAt[1])]
    fullMonthName = calendar.month_name[int(splitCreatedAt[1])]

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    no_border = workbook.add_format({'border': 1, 'border_color': '#FFFFFF'})
    worksheet.set_column(0, 16383, None, no_border)

    border = workbook.add_format({'border': 2})
    border_align_center = workbook.add_format({'border': 2, 'align': 'center'})
    border_align_center_bold = workbook.add_format(
        {'border': 2, 'align': 'center', "bold": True})
    border_align_right = workbook.add_format({'border': 2, 'align': 'right'})
    border_align_right_num_format = workbook.add_format(
        {'border': 2, 'align': 'right', 'num_format': '₹ #,##0'})
    align_center = workbook.add_format(
        {'align': 'center', 'border': 1, 'border_color': '#FFFFFF'})
    align_right = workbook.add_format(
        {'align': 'right', 'border': 1, 'border_color': '#FFFFFF'})
    align_right_bold = workbook.add_format(
        {'align': 'right', 'border': 1, 'border_color': '#FFFFFF', "bold": True})
    font_size = workbook.add_format()
    num_format = workbook.add_format({'num_format': '₹ #,##0'})
    align_center_bold = workbook.add_format(
        {'align': 'center', 'border': 1, 'border_color': '#FFFFFF', 'bold': True})

    border.set_font_size(15)
    border_align_right.set_font_size(15)
    border_align_center.set_font_size(15)
    border_align_center_bold.set_font_size(15)
    font_size.set_font_size(15)
    align_right.set_font_size(15)
    align_right_bold.set_font_size(15)
    align_center.set_font_size(15)
    align_center_bold.set_font_size(15)
    border_align_right_num_format.set_font_size(15)
    num_format.set_font_size(15)

    worksheet.write(2, 0, 'No', border_align_center)
    worksheet.write(2, 1, 'Name', border_align_center)
    worksheet.write(2, 2, 'Flat no', border_align_center)
    worksheet.write(2, 3, 'Amount', border_align_center)
    worksheet.write(2, 4, 'Date', border_align_center)

    worksheet.write(2, 6, 'No', border_align_center)
    worksheet.write(2, 7, 'Description', border_align_center)
    worksheet.write(2, 8, 'Vr no', border_align_center)
    worksheet.write(2, 9, 'Date', border_align_center)
    worksheet.write(2, 10, 'Amount', border_align_center)
    worksheet.write(2, 11, 'Purpose', border_align_center)

    worksheet.set_column(1, 1, 40, no_border)  # Name
    worksheet.set_column(2, 2, 15, no_border)  # Flat No
    worksheet.set_column(3, 3, 15, no_border)  # Amount
    worksheet.set_column(4, 4, 15, no_border)  # Date

    worksheet.set_column(7, 7, 60, no_border)  # Expense Name
    worksheet.set_column(9, 9, 18, no_border)  # Expense Date
    worksheet.set_column(10, 10, 15, no_border)  # Expense Amount
    worksheet.set_column(11, 11, 45, no_border)  # Expense Reason

    incomeTable = db.query(IncomeTable).filter(
        IncomeTable.createdAt == createdAt).order_by(IncomeTable.date).all()
    row = 3
    for income in incomeTable:
        worksheet.write(row, 0, row - 2,  border_align_center)
        worksheet.write(row, 1, income.name,  border)
        worksheet.write(row, 2, income.flatNo,  border_align_center)
        worksheet.write(row, 3, income.amount, border_align_right_num_format)
        worksheet.write(row, 4, income.date,  border_align_center)
        row += 1

    lastIncomeRow = row

    expenseTable = db.query(ExpenseTable).filter(
        ExpenseTable.createdAt == createdAt).order_by(ExpenseTable.expenseDate).all()

    row = 3
    for expense in expenseTable:
        worksheet.write(row, 6, row - 2, border_align_center)
        worksheet.write(row, 7, expense.expenseName, border)
        worksheet.write(row, 8, expense.vrNo, border_align_center)
        worksheet.write(row, 9, expense.expenseDate, border_align_center)
        worksheet.write(row, 10, expense.expenseAmount,
                        border_align_right_num_format)
        worksheet.write(row, 11, expense.expenseReason, border)
        row += 1

    lastExpenseRow = row
    totalRow = max(lastIncomeRow, lastExpenseRow)
    for i in range(12):  # 11
        if i == 5:
            continue
        worksheet.write_blank(totalRow, i, '', border_align_center)
    totalRow += 1

    worksheet.write(totalRow, 2, "Total", border_align_center_bold)
    worksheet.write(
        totalRow, 3, f"=SUM(D2:D{lastIncomeRow})", border_align_right_num_format)
    worksheet.write(totalRow, 9, "Total", border_align_center_bold)
    worksheet.write(
        totalRow, 10, f"=SUM(K3:k{lastExpenseRow})", border_align_right_num_format)

    worksheet.write(totalRow + 2, 9, "Income Total", border_align_center_bold)
    worksheet.write(totalRow + 2, 10,
                    f"=D{totalRow+1}", border_align_right_num_format)

    worksheet.write(totalRow + 3, 9, "Expense Total", border_align_center_bold)
    worksheet.write(totalRow + 3, 10,
                    f"=K{totalRow+1}", border_align_right_num_format)

    worksheet.merge_range('A1:C1', 'INCOME', align_center_bold)
    worksheet.merge_range('H1:J1', 'EXPENSE', align_center_bold)

    worksheet.write('D1', 'Month:', align_right_bold)
    worksheet.write('E1', f"{monthName}, {splitCreatedAt[0]}", font_size)
    worksheet.write('K1', 'Month:', align_right_bold)
    worksheet.write('L1', f"{monthName}, {splitCreatedAt[0]}", font_size)

    cfQuery = db.query(CarryForward).filter(
        CarryForward.createdAt == createdAt)
    cfData = cfQuery.first()
    if cfData is None:
        cfData = CarryForward(**{"cf": 0, "nextMonthCF": 0})

    worksheet.merge_range(
        'A2:C2', 'C/F OF PREVIOUS MONTH:', align_right_bold)
    worksheet.write('D2', cfData.cf, border_align_right_num_format)

    worksheet.write(totalRow + 4, 9, "Balance", border_align_center_bold)
    worksheet.write(totalRow + 4, 10,
                    cfData.nextMonthCF, border_align_right_num_format)

    workbook.close()
    output.seek(0)

    headers = {
        'Content-Type': 'application/octet-stream',
        'Content-Disposition': f'attachment; filename="{fullMonthName} - {splitCreatedAt[0]}.xlsx"',
    }
    return StreamingResponse(output, headers=headers)


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
    cfTableData = tableDict["cf"]

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

    return {"income": newIncomeTables, "expense": newExpenseTables, "cf": newCFTables}


@router.delete("/", dependencies=[Depends(allow)])
async def delete_entries(ids: schemas.EntriesToDelete, db: Session = Depends(get_db)):

    for value in ids.income:
        deleteQuery = db.query(IncomeTable).filter(IncomeTable.id == value)
        deleteEntry = deleteQuery.first()
        if deleteEntry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Entry with id: {value} Doesnt Exist")
        deleteQuery.delete()

    for value in ids.expense:
        deleteQuery = db.query(ExpenseTable).filter(
            ExpenseTable.id == value)
        deleteEntry = deleteQuery.first()
        if deleteEntry is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Entry with id: {value} Doesnt Exist")
        deleteQuery.delete()

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
