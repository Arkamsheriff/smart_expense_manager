from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.recurring.recurring_manager import RecurringExpenseManager


router = APIRouter(
    prefix="/api/recurring",
    tags=["Recurring Expenses"]
)

manager = RecurringExpenseManager()


class RecurringExpenseCreate(BaseModel):
    description: str
    amount: float
    category: str
    frequency: str
    start_date: str
    end_date: str | None = None
    active: bool = True


class RecurringExpenseUpdate(BaseModel):
    description: str
    amount: float
    category: str
    frequency: str
    start_date: str
    end_date: str | None = None
    active: bool = True


class RecurringExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    frequency: str
    start_date: str
    end_date: str | None
    active: bool


@router.get("", response_model=list[RecurringExpenseResponse])
def get_recurring_expenses():
    return manager.get_all_recurring_expenses()


@router.get("/{expense_id}", response_model=RecurringExpenseResponse)
def get_recurring_expense(expense_id: int):
    expense = manager.get_recurring_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Recurring expense not found"
        )

    return expense


@router.post("", response_model=RecurringExpenseResponse)
def create_recurring_expense(data: RecurringExpenseCreate):
    try:
        return manager.create_recurring_expense(
            description=data.description,
            amount=data.amount,
            category=data.category,
            frequency=data.frequency,
            start_date=data.start_date,
            end_date=data.end_date,
            active=data.active
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/{expense_id}", response_model=RecurringExpenseResponse)
def update_recurring_expense(
    expense_id: int,
    data: RecurringExpenseUpdate
):
    try:
        updated = manager.update_recurring_expense(
            expense_id=expense_id,
            description=data.description,
            amount=data.amount,
            category=data.category,
            frequency=data.frequency,
            start_date=data.start_date,
            end_date=data.end_date,
            active=data.active
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Recurring expense not found"
            )

        return manager.get_recurring_expense(expense_id)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{expense_id}")
def delete_recurring_expense(expense_id: int):
    deleted = manager.delete_recurring_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Recurring expense not found"
        )

    return {
        "message": "Recurring expense deleted successfully"
    }


@router.patch("/{expense_id}/toggle", response_model=RecurringExpenseResponse)
def toggle_recurring_expense(expense_id: int):
    updated = manager.toggle_active(expense_id)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Recurring expense not found"
        )

    return manager.get_recurring_expense(expense_id)


@router.get(
    "/{expense_id}/next-due",
    response_model=str | None
)
def get_next_due_date(expense_id: int):
    expense = manager.get_recurring_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Recurring expense not found"
        )

    return manager.get_next_due_date(expense_id)