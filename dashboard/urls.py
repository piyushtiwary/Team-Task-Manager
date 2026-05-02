from django.urls import path
from .views import DashboardSummaryView

urlpatterns = [
    # API endpoint (under /api/dashboard/)
    path("summary/", DashboardSummaryView.as_view(), name="dashboard-api"),
]
