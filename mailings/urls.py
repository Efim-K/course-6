from django.urls import path

from mailings.apps import MailingsConfig
from mailings.views import MailingsListView, MailingsDetailView, MailingsCreateView, MailingsUpdateView, \
    MailingsDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingsListView.as_view(), name='mailings_list'),
    path('<int:pk>/', MailingsDetailView.as_view(), name='mailings_view'),
    path('create/', MailingsCreateView.as_view(), name='mailings_create'),
    path('<int:pk>/update/', MailingsUpdateView.as_view(), name='mailings_update'),
    path('<int:pk>/delete/', MailingsDeleteView.as_view(), name='mailings_delete'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
]
