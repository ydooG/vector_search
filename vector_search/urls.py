from django.contrib import admin
from django.urls import path, include

api_urls = [
    path('', include('search.api.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search.urls')),
    path('api/', include(api_urls))
]
