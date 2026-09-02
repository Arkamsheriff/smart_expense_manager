from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.goals.goal_manager import GoalManager


router = APIRouter(
    prefix="/api/goals",
    tags=["Financial Goals"]
)

manager = GoalManager()


class GoalCreate(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    target_date: Optional[str] = None


class GoalUpdate(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    target_date: Optional[str] = None


class GoalResponse(BaseModel):
    id: int
    name: str
    target_amount: float
    current_amount: float
    target_date: Optional[str]
    remaining: float
    percentComplete: float


def goal_to_response(goal):
    if goal is None:
        return None

    remaining = max(
        goal.target_amount - goal.current_amount,
        0
    )

    if goal.target_amount <= 0:
        percent_complete = 0.0
    else:
        percent_complete = min(
            (goal.current_amount / goal.target_amount) * 100,
            100.0
        )

    return {
        "id": goal.id,
        "name": goal.name,
        "target_amount": goal.target_amount,
        "current_amount": goal.current_amount,
        "target_date": goal.target_date,
        "remaining": remaining,
        "percentComplete": percent_complete
    }


@router.get("", response_model=list[GoalResponse])
def get_goals():
    goals = manager.get_all_goals()

    return [
        goal_to_response(goal)
        for goal in goals
    ]


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int):
    goal = manager.get_goal(goal_id)

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal_to_response(goal)


@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED
)
def create_goal(data: GoalCreate):
    if data.target_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Target amount must be greater than 0"
        )

    if data.current_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Current amount cannot be negative"
        )

    if not data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Goal name cannot be empty"
        )

    goal = manager.create_goal(
        name=data.name,
        target_amount=data.target_amount,
        current_amount=data.current_amount,
        target_date=data.target_date
    )

    return goal_to_response(goal)


@router.put(
    "/{goal_id}",
    response_model=GoalResponse
)
def update_goal(goal_id: int, data: GoalUpdate):
    existing = manager.get_goal(goal_id)

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if data.target_amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Target amount must be greater than 0"
        )

    if data.current_amount < 0:
        raise HTTPException(
            status_code=400,
            detail="Current amount cannot be negative"
        )

    if not data.name.strip():
        raise HTTPException(
            status_code=400,
            detail="Goal name cannot be empty"
        )

    manager.update_goal(
        goal_id=goal_id,
        name=data.name,
        target_amount=data.target_amount,
        current_amount=data.current_amount,
        target_date=data.target_date
    )

    updated = manager.get_goal(goal_id)

    return goal_to_response(updated)


@router.delete(
    "/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_goal(goal_id: int):
    deleted = manager.delete_goal(goal_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return None