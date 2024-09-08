from django.shortcuts import render
from django.views.generic import ListView

from mailings.models import Mailings


# Create your views here.
class MailingsListView(ListView):
    model = Mailings
