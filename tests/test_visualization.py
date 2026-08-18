import matplotlib

matplotlib.use("Agg")

from app.reports.visualization import VisualizationService


def test_category_bar_chart():
    service = VisualizationService()

    data = {
        "Food": 350.75,
        "Housing": 500.00,
        "Transport": 100.00
    }

    service.category_bar_chart(data)


def test_category_pie_chart():
    service = VisualizationService()

    data = {
        "Food": 350.75,
        "Housing": 500.00,
        "Transport": 100.00
    }

    service.category_pie_chart(data)