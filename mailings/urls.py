from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingsListView, MailingsDetailView, MailingsCreateView, MailingsUpdateView, \
    MailingsDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingsListView.as_view(), name='mailings_list'),
    path('<int:pk>/', MailingsDetailView.as_view(), name='mailings_view'),
    path('create/', MailingsCreateView.as_view(), name='mailings_create'),
    path('<int:pk>/update/', MailingsUpdateView.as_view(), name='mailings_update'),
    path('<int:pk>/delete/', MailingsDeleteView.as_view(), name='mailings_delete'),
]
