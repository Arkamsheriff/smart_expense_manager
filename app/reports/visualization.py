import matplotlib.pyplot as plt


class VisualizationService:

    def category_bar_chart(self, category_summary):
        if not category_summary:
            print("No data available for chart.")
            return

        categories = list(category_summary.keys())
        amounts = list(category_summary.values())

        plt.figure(figsize=(10, 6))

        plt.bar(categories, amounts)

        plt.title("Expense by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")

        plt.xticks(rotation=45)

        plt.tight_layout()

        return plt.gcf()

    def category_pie_chart(self, category_summary):
        if not category_summary:
            print("No data available for chart.")
            return

        categories = list(category_summary.keys())
        amounts = list(category_summary.values())

        plt.figure(figsize=(8, 8))

        plt.pie(
            amounts,
            labels=categories,
            autopct="%1.1f%%"
        )

        plt.title("Expense Distribution by Category")

        return plt.gcf()