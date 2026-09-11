from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import psycopg

from app.budget.budget_manager import BudgetManager
from app.database.connection import get_connection
from app.api.auth import CurrentUser


router = APIRouter(
    prefix="/api/budgets",
    tags=["Budgets"]
)

manager = BudgetManager()


class BudgetCreate(BaseModel):
    category: str
    amount: float
    period: str = "monthly"


class BudgetUpdate(BaseModel):
    category: str
    amount: float
    period: str = "monthly"


class BudgetResponse(BaseModel):
    id: int
    category: str
    amount: float
    period: str
    spent: float
    remaining: float
    percentUsed: float


def build_budget_response(budget, user_id):
    connection = get_connection()

    try:
        placeholder = (
            "%s"
            if isinstance(connection, psycopg.Connection)
            else "?"
        )

        row = connection.execute(
            f"""
            SELECT COALESCE(SUM(amount), 0) AS spent
            FROM expenses
            WHERE LOWER(category) = LOWER({placeholder})
              AND user_id = {placeholder}
            """,
            (
                budget.month,
                user_id
            )
        ).fetchone()

        spent = float(row["spent"] or 0)

    finally:
        connection.close()

    remaining = float(budget.amount) - spent

    if budget.amount > 0:
        percent_used = (
            spent / float(budget.amount)
        ) * 100
    else:
        percent_used = 0

    return {
        "id": budget.id,
        "category": budget.month,
        "amount": float(budget.amount),
        "period": "monthly",
        "spent": spent,
        "remaining": remaining,
        "percentUsed": percent_used
    }


@router.get("", response_model=list[BudgetResponse])
def get_budgets(current_user: CurrentUser):
    user_id = current_user["id"]

    budgets = manager.get_all_budgets(user_id)

    return [
        build_budget_response(
            budget,
            user_id
        )
        for budget in budgets
    ]


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: int,
    current_user: CurrentUser
):
    user_id = current_user["id"]

    budgets = manager.get_all_budgets(user_id)

    for budget in budgets:
        if budget.id == budget_id:
            return build_budget_response(
                budget,
                user_id
            )

    raise HTTPException(
        status_code=404,
        detail="Budget not found"
    )


@router.post("", response_model=BudgetResponse)
def create_budget(
    data: BudgetCreate,
    current_user: CurrentUser
):
    user_id = current_user["id"]

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget amount must be greater than 0"
        )

    if data.period.lower() != "monthly":
        raise HTTPException(
            status_code=400,
            detail="Only monthly budgets are currently supported"
        )

    category = data.category.strip()

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Budget category cannot be empty"
        )

    try:
        budget = manager.set_budget(
            user_id=user_id,
            month=category,
            amount=data.amount
        )

        return build_budget_response(
            budget,
            user_id
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    data: BudgetUpdate,
    current_user: CurrentUser
):
    user_id = current_user["id"]

    if data.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Budget amount must be greater than 0"
        )

    if data.period.lower() != "monthly":
        raise HTTPException(
            status_code=400,
            detail="Only monthly budgets are currently supported"
        )

    budgets = manager.get_all_budgets(user_id)

    existing = None

    for budget in budgets:
        if budget.id == budget_id:
            existing = budget
            break

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    category = data.category.strip()

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Budget category cannot be empty"
        )

    try:
        updated = manager.update_budget(
            user_id=user_id,
            budget_id=budget_id,
            month=category,
            amount=data.amount
        )

        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Budget not found"
            )

        updated_budget = manager.get_budget(
            user_id,
            category
        )

        if updated_budget is None:
            raise HTTPException(
                status_code=404,
                detail="Updated budget not found"
            )

        return build_budget_response(
            updated_budget,
            user_id
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    current_user: CurrentUser
):
    user_id = current_user["id"]

    deleted = manager.delete_budget(
        user_id,
        budget_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    return {
        "message": "Budget deleted successfully"
    }