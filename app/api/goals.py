from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.api.auth import CurrentUser
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
        "target_amount": float(goal.target_amount),
        "current_amount": float(goal.current_amount),
        "target_date": goal.target_date,
        "remaining": float(remaining),
        "percentComplete": float(percent_complete)
    }


@router.get("", response_model=list[GoalResponse])
def get_goals(current_user: CurrentUser):

    user_id = current_user["id"]

    goals = manager.get_all_goals(user_id)

    return [
        goal_to_response(goal)
        for goal in goals
    ]


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    current_user: CurrentUser
):

    user_id = current_user["id"]

    goal = manager.get_goal(
        goal_id,
        user_id
    )

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
def create_goal(
    data: GoalCreate,
    current_user: CurrentUser
):

    user_id = current_user["id"]

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
        user_id=user_id,
        name=data.name.strip(),
        target_amount=data.target_amount,
        current_amount=data.current_amount,
        target_date=data.target_date
    )

    return goal_to_response(goal)


@router.put(
    "/{goal_id}",
    response_model=GoalResponse
)
def update_goal(
    goal_id: int,
    data: GoalUpdate,
    current_user: CurrentUser
):

    user_id = current_user["id"]

    existing = manager.get_goal(
        goal_id,
        user_id
    )

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

    updated = manager.update_goal(
        goal_id=goal_id,
        user_id=user_id,
        name=data.name.strip(),
        target_amount=data.target_amount,
        current_amount=data.current_amount,
        target_date=data.target_date
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    updated_goal = manager.get_goal(
        goal_id,
        user_id
    )

    if updated_goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal_to_response(updated_goal)


@router.delete(
    "/{goal_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_goal(
    goal_id: int,
    current_user: CurrentUser
):

    user_id = current_user["id"]

    deleted = manager.delete_goal(
        goal_id,
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return None