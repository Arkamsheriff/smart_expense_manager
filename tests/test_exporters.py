from datetime import datetime

from app.expense import Expense
from app.exports.csv_exporter import CSVExporter


def test_csv_export(tmp_path):

    expenses = [
        Expense(
            1,
            "Rent",
            500.00,
            "Housing",
            datetime(2026, 8, 19, 20, 15, 31)
        ),
        Expense(
            2,
            "Food",
            200.00,
            "Food",
            datetime(2026, 8, 19, 20, 20, 10)
        )
    ]

    file_path = tmp_path / "expenses.csv"

    exporter = CSVExporter()

    exporter.export(expenses, file_path)

    assert file_path.exists()

    content = file_path.read_text(encoding="utf-8")

    assert "ID,Description,Amount,Category,Created At" in content
    assert "1,Rent,500.00,Housing,2026-08-19 20:15:31" in content
    assert "2,Food,200.00,Food,2026-08-19 20:20:10" in content