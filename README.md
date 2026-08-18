# Smart Expense Manager

A Python-based expense management and analytics application built with SQLite, automated testing, reporting, and data visualization.

## 🚀 Features

- Add expenses
- Update expenses
- Delete expenses
- List all expenses
- Calculate total expenses
- Calculate category-wise totals
- Automatic expense ID generation
- Expense validation
- Date and time tracking
- Daily expense reports
- Weekly expense reports
- Monthly expense reports
- Category spending analysis
- Spending statistics
- Category bar charts
- Category pie charts
- SQLite database persistence
- Automated testing with Pytest

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| SQLite | Database |
| Pytest | Automated testing |
| Matplotlib | Data visualization |
| Git | Version control |
| GitHub | Source code management |

## 📁 Project Structure

```text
smart_expense_manager/
│
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── repository.py
│   │
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── report_service.py
│   │   └── visualization.py
│   │
│   ├── __init__.py
│   ├── expense.py
│   ├── expense_manager.py
│   ├── main.py
│   └── validators.py
│
├── tests/
│   ├── test_expense_manager.py
│   ├── test_reports.py
│   ├── test_repository.py
│   ├── test_validators.py
│   └── test_visualization.py
│
├── data/
├── reports/
├── .gitignore
├── README.md
└── requirements.txt