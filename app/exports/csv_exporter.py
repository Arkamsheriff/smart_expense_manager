import csv


class CSVExporter:

    def export(self, expenses, file_path):
        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "ID",
                "Description",
                "Amount",
                "Category",
                "Created At"
            ])

            for expense in expenses:
                writer.writerow([
                    expense.id,
                    expense.description,
                    f"{expense.amount:.2f}",
                    expense.category,
                    expense.created_at.strftime("%Y-%m-%d %H:%M:%S")
                ])