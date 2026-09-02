from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.repository import initialize_database
from app.api.expenses import router as expenses_router
from app.api.dashboard import router as dashboard_router
from app.api.income import router as income_router
from app.api.recurring import router as recurring_router
from app.api.budgets import router as budgets_router
from app.api.goals import router as goals_router
from app.api.reports import router as reports_router


initialize_database()

app = FastAPI(
    title="Smart Expense Manager API",
    description="REST API for Smart Expense Manager",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(expenses_router)
app.include_router(income_router)
app.include_router(dashboard_router)
app.include_router(recurring_router)
app.include_router(budgets_router)
app.include_router(goals_router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {
        "message": "Smart Expense Manager API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }