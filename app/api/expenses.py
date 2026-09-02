from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.expense_manager import ExpenseManager


router = APIRouter(
    prefix="/api/expenses",
    tags=["Expenses"]
)

manager = ExpenseManager()


class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)


class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    created_at: str


class ExpenseUpdate(BaseModel):
    description: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)


def expense_to_response(expense):
    return ExpenseResponse(
        id=expense.id,
        description=expense.description,
        amount=float(expense.amount),
        category=expense.category,
        created_at=expense.created_at.isoformat()
    )


@router.get("", response_model=list[ExpenseResponse])
def get_expenses():
    expenses = manager.list_expenses()

    return [
        expense_to_response(expense)
        for expense in expenses
    ]


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int):
    expenses = manager.list_expenses()

    for expense in expenses:
        if expense.id == expense_id:
            return expense_to_response(expense)

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate):
    created = manager.add_expense(
        expense.description,
        expense.amount,
        expense.category
    )

    return expense_to_response(created)


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate
):
    updated = manager.update_expense(
        expense_id,
        expense.description,
        expense.amount,
        expense.category
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expenses = manager.list_expenses()

    for existing in expenses:
        if existing.id == expense_id:
            return expense_to_response(existing)

    raise HTTPException(
        status_code=404,
        detail="Expense not found"
    )


@router.delete("/{expense_id}")
def delete_expense(expense_id: int):
    deleted = manager.delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }


@router.get("/total/summary")
def get_total_expenses():
    total = manager.total_expenses()

    return {
        "total": float(total)
    }


@router.get("/category/{category}")
def get_category_total(category: str):
    total = manager.category_total(category)

    return {
        "category": category,
        "total": float(total)
    }


@router.get("/search/{keyword}")
def search_expenses(keyword: str):
    expenses = manager.search_expenses(keyword)

    return [
        expense_to_response(expense)
        for expense in expenses
    ]


@router.get("/filter/category/{category}")
def filter_by_category(category: str):
    expenses = manager.filter_expenses_by_category(category)

    return [
        expense_to_response(expense)
        for expense in expenses
    ]


@router.get("/filter/amount")
def filter_by_amount(
    minimum: float,
    maximum: float
):
    if minimum < 0 or maximum < 0:
        raise HTTPException(
            status_code=400,
            detail="Amounts cannot be negative"
        )

    if minimum > maximum:
        raise HTTPException(
            status_code=400,
            detail="Minimum amount cannot exceed maximum amount"
        )

    expenses = manager.filter_expenses_by_amount(
        minimum,
        maximum
    )

    return [
        expense_to_response(expense)
        for expense in expenses
    ]