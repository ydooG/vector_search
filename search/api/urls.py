from django.urls import path

from search.api.views import MakeSearchView

app_name = 'search_api'

urlpatterns = [
    path('search/', MakeSearchView.as_view(), name='search')
]
