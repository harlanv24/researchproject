# arxiv_api/urls.py
from django.urls import path
from .views import ArxivSearchView

urlpatterns = [
    path('search/', ArxivSearchView.as_view(), name='arxiv-search'),
]