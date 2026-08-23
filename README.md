# Smart Expense Manager

A Python-based personal expense management and analytics application built with **SQLite, Pytest, Matplotlib, and modular software architecture**.

The application allows users to manage expenses, generate time-based reports, analyze spending patterns, visualize category-wise spending, and export expense data to CSV.

---

## 🚀 Features

### 💰 Expense Management

- Add expenses
- Update existing expenses
- Delete expenses
- List all expenses
- Automatic expense ID generation
- Date and time tracking
- Persistent SQLite database storage

### 📊 Expense Analysis

- Calculate total expenses
- Calculate category-wise expenses
- Analyze monthly spending
- Generate category spending summaries
- Calculate spending statistics
  - Number of expenses
  - Total spending
  - Average expense
  - Highest expense
  - Lowest expense

### 📅 Reports

- Today's expenses
- Today's total spending
- Weekly expense reports
- Monthly expense reports
- Category spending summaries
- Monthly spending statistics

### 📈 Data Visualization

- Category-wise bar charts
- Category-wise pie charts
- Matplotlib-based visualization

### 📤 Data Export

- Export all expenses to CSV
- Structured CSV output for further analysis

### 🛡️ Validation

- Description validation
- Amount validation
- Category validation
- Expense ID validation
- Input error handling

### 🧪 Testing

- Automated testing using Pytest
- Unit tests for expense management
- Repository/database tests
- Validation tests
- Report service tests
- Visualization tests
- Main application tests
- CSV exporter tests

---

## 🛠️ Technology Stack

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

---

## 🏗️ Application Architecture

The project follows a modular architecture that separates application logic, database operations, reporting, validation, visualization, and data export.

```text
User
 │
 ▼
CLI Interface
 │
 ▼
Expense Manager
 │
 ├──────────────► Validators
 │
 ├──────────────► Repository
 │                    │
 │                    ▼
 │                 SQLite
 │
 ├──────────────► Report Service
 │                    │
 │                    ▼
 │                 Analytics
 │
 ├──────────────► Visualization
 │                    │
 │                    ▼
 │                 Matplotlib
 │
 └──────────────► CSV Exporter
                      │
                      ▼
                    CSV File