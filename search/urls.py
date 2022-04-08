from django.urls import path

from search.views import IndexView

app_name = 'search'

urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
