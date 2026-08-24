# Smart Expense Manager

A Python-based personal expense management and analytics application built using **Python, SQLite, Pytest, Matplotlib, and modular software architecture**.

The application allows users to manage expenses, generate reports, analyze spending patterns, visualize category-wise spending, search and filter expenses, and export expense data to CSV.

---

## Features

### Expense Management

- Add expenses
- Update existing expenses
- Delete expenses
- List all expenses
- Automatic expense ID generation
- Date and time tracking
- Persistent SQLite database storage

### Expense Analysis

- Calculate total expenses
- Calculate category-wise expenses
- Analyze monthly spending
- Generate category spending summaries
- Calculate spending statistics:
  - Number of expenses
  - Total spending
  - Average expense
  - Highest expense
  - Lowest expense

### Reports

- Today's expenses
- Today's total spending
- Weekly expense reports
- Monthly expense reports
- Category spending summaries
- Monthly spending statistics

### Search and Filtering

- Search expenses by description
- Filter expenses by category
- Filter expenses by amount range
- Case-insensitive category filtering
- Display filtered results through the CLI

### Data Visualization

- Category-wise bar charts
- Category-wise pie charts
- Matplotlib-based visualization

### Data Export

- Export all expenses to CSV
- Structured CSV output
- Automatic report directory creation

### Input Validation

- Description validation
- Amount validation
- Category validation
- Expense ID validation
- Invalid input handling
- Invalid amount-range handling

### Testing

- Automated testing using Pytest
- Repository/database tests
- Expense manager tests
- Validation tests
- Report service tests
- Visualization tests
- Main application tests
- CSV exporter tests
- Error-handling tests
- Code coverage analysis

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| SQLite | Database persistence |
| Pytest | Automated testing |
| pytest-cov | Code coverage analysis |
| Matplotlib | Data visualization |
| CSV | Expense data export |
| Git | Version control |
| GitHub | Source code management |
| GitHub Actions | Continuous Integration |

---

## Application Architecture

The project follows a modular architecture that separates the CLI interface, business logic, database operations, reporting, validation, visualization, and data export.

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   CLI Interface  │
                         │    main.py       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Expense Manager  │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
      ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
      │  Validators  │    │  Repository  │    │Report Service│
      └──────────────┘    └──────┬───────┘    └──────┬───────┘
                                 │                   │
                                 ▼                   ▼
                         ┌──────────────┐    ┌──────────────┐
                         │    SQLite    │    │  Analytics   │
                         └──────────────┘    └──────────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │  Visualization   │
                                          │    Matplotlib    │
                                          └──────────────────┘

                         ┌──────────────────┐
                         │   CSV Exporter   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    CSV File      │
                         └──────────────────┘
```

---

## Project Structure

```text
smart_expense_manager/
│
├── app/
│   ├── database/
│   │   ├── connection.py
│   │   ├── repository.py
│   │   └── __init__.py
│   │
│   ├── exports/
│   │   ├── csv_exporter.py
│   │   └── __init__.py
│   │
│   ├── reports/
│   │   ├── report_service.py
│   │   ├── visualization.py
│   │   └── __init__.py
│   │
│   ├── expense.py
│   ├── expense_manager.py
│   ├── main.py
│   ├── validators.py
│   └── __init__.py
│
├── tests/
│   ├── test_expense_manager.py
│   ├── test_exporters.py
│   ├── test_main.py
│   ├── test_reports.py
│   ├── test_repository.py
│   ├── test_validators.py
│   └── test_visualization.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── data/
│   └── expenses.db
│
├── reports/
│   └── expenses.csv
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Arkamsheriff/smart_expense_manager.git
```

### 2. Navigate to the project

```bash
cd smart_expense_manager
```

### 3. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Running the Application

Start the application with:

```bash
python -m app.main
```

The application displays the main menu:

```text
================================
      SMART EXPENSE MANAGER
================================
1. Add Expense
2. Delete Expense
3. Total Expenses
4. Category Total
5. List Expenses
6. Update Expense
7. Reports
8. Export
9. Search & Filter
10. Exit
================================
```

---

## Expense Management

### Add Expense

Select:

```text
1. Add Expense
```

Then enter:

```text
Description
Amount
Category
```

Example:

```text
Description: Monthly Rent
Amount: 15000
Category: Housing
```

The application automatically generates the expense ID and records the creation date and time.

---

### Update Expense

Select:

```text
6. Update Expense
```

Enter the expense ID and provide the new:

- Description
- Amount
- Category

---

### Delete Expense

Select:

```text
2. Delete Expense
```

Enter the expense ID to remove the expense.

---

## Reports

Select:

```text
7. Reports
```

Available reports:

```text
1. Today's Expenses
2. Today's Total
3. This Week
4. This Month
5. Category Summary
6. Spending Statistics
7. Charts
8. Back
```

### Spending Statistics

The application calculates:

- Number of expenses
- Total spending
- Average expense
- Highest expense
- Lowest expense

---

## Search and Filtering

Select:

```text
9. Search & Filter
```

Available options:

```text
1. Search by Description
2. Filter by Category
3. Filter by Amount Range
4. Back
```

### Description Search

Searches expense descriptions using a keyword.

Example:

```text
Enter description keyword: Rent
```

### Category Filter

Filters expenses by category.

Category matching is case-insensitive.

For example:

```text
Food
food
FOOD
```

are treated as the same category when filtering and calculating category totals.

### Amount Range

Filters expenses between a minimum and maximum amount.

Example:

```text
Enter minimum amount: 200
Enter maximum amount: 1000
```

---

## Data Visualization

The application provides two chart types:

### Category Bar Chart

Displays spending for each category using a bar chart.

### Category Pie Chart

Displays the percentage distribution of spending between categories.

Both charts are generated using **Matplotlib**.

---

## CSV Export

Select:

```text
8. Export
```

Then:

```text
1. Export All Expenses to CSV
```

The application creates:

```text
reports/expenses.csv
```

Example:

```csv
ID,Description,Amount,Category,Created At
1,Monthly Rent,15000.00,Housing,2026-08-24 10:30:15
2,Groceries,2500.00,Food,2026-08-24 11:00:20
```

---

## Database

The application uses **SQLite** for persistent data storage.

The database is stored at:

```text
data/expenses.db
```

The database directory is automatically created when required.

The repository layer handles:

- Database initialization
- Adding expenses
- Retrieving expenses
- Updating expenses
- Deleting expenses
- Date-based queries
- Description searches
- Category filtering
- Amount-range filtering

---

## Testing

The project uses **Pytest** for automated testing.

Run the complete test suite:

```bash
python -m pytest
```

Current test suite:

```text
76 passed
```

---

## Code Coverage

Generate the coverage report:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Current coverage:

```text
TOTAL    471 statements    3 missed    99%
```

The application currently maintains approximately **99% code coverage**.

---

## Continuous Integration

GitHub Actions is configured to automatically run the test suite whenever changes are pushed to the `main` branch or a pull request is created.

Workflow:

```text
Developer
    │
    ▼
Git Push / Pull Request
    │
    ▼
GitHub Actions
    │
    ▼
Install Python
    │
    ▼
Install Dependencies
    │
    ▼
Run Pytest
    │
    ▼
Generate Coverage
    │
    ▼
Coverage >= 90% ?
    │
   ┌┴─────────────┐
   │              │
  YES             NO
   │              │
   ▼              ▼
  PASS           FAIL
```

The CI pipeline requires at least **90% code coverage**.

---

## Development Workflow

The project follows a test-driven and modular development workflow:

```text
Feature Development
        │
        ▼
Implement Code
        │
        ▼
Write / Update Tests
        │
        ▼
Run Pytest
        │
        ▼
Run Coverage
        │
        ▼
Review Results
        │
        ▼
Git Commit
        │
        ▼
Git Push
        │
        ▼
GitHub Actions
        │
        ▼
CI Validation
```

---

## Quality Metrics

| Metric | Current Status |
|---|---|
| Automated Tests | 76 |
| Test Result | 76 Passed |
| Overall Coverage | 99% |
| Repository Coverage | 100% |
| Main Application Coverage | 99% |
| CI Coverage Threshold | 90% |
| Database | SQLite |
| Visualization | Matplotlib |
| Export Format | CSV |

---

## Design Principles

The project follows several software engineering principles:

- Modular architecture
- Separation of responsibilities
- Repository pattern for database access
- Dedicated validation functions
- Dedicated reporting service
- Dedicated visualization service
- Dedicated CSV exporter
- Automated unit testing
- High code coverage
- Continuous Integration
- Error handling for database operations
- Reusable business logic

---

## Future Improvements

Possible future enhancements include:

- Budget management
- Recurring expenses
- Date-range filtering
- Multiple export formats
- Import expenses from CSV
- Advanced analytics
- Dashboard interface
- User authentication
- Database migrations
- REST API
- Web-based interface
- Cloud database support

---

## License

This project is developed as a software engineering project for learning, development, testing, and demonstration purposes.