from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingsListView, MailingsDetailView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingsListView.as_view(), name='mailings_list'),
    path('<int:pk>/', MailingsDetailView.as_view(), name='mailings_view'),
]
