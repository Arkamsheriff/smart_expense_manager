from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.income.income_manager import IncomeManager


router = APIRouter(
    prefix="/api/income",
    tags=["Income"]
)

manager = IncomeManager()


class IncomeCreate(BaseModel):
    description: str
    amount: float
    category: str


class IncomeUpdate(BaseModel):
    description: str
    amount: float
    category: str


class IncomeResponse(BaseModel):
    id: int
    description: str
    amount: float
    category: str
    created_at: datetime


def income_to_dict(income):
    return {
        "id": income.id,
        "description": income.description,
        "amount": income.amount,
        "category": income.category,
        "created_at": income.created_at,
    }


@router.get("")
def get_income():
    incomes = manager.get_all_income()

    return [
        income_to_dict(income)
        for income in incomes
    ]


@router.post("", status_code=201)
def create_income(data: IncomeCreate):
    income = manager.create_income(
        data.description,
        data.amount,
        data.category
    )

    return income_to_dict(income)


@router.get("/{income_id}")
def get_income_by_id(income_id: int):
    income = manager.get_income(income_id)

    if income is None:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    return income_to_dict(income)


@router.put("/{income_id}")
def update_income(
    income_id: int,
    data: IncomeUpdate
):
    result = manager.update_income(
        income_id,
        data.description,
        data.amount,
        data.category
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    income = manager.get_income(income_id)

    return income_to_dict(income)


@router.delete("/{income_id}")
def delete_income(income_id: int):
    result = manager.delete_income(income_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Income not found"
        )

    return {
        "message": "Income deleted successfully"
    }


@router.get("/total/summary")
def get_total_income():
    return {
        "total": manager.total_income()
    }


@router.get("/category/{category}")
def get_income_by_category(category: str):
    incomes = manager.get_income_by_category(category)

    return [
        income_to_dict(income)
        for income in incomes
    ]