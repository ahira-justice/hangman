from django.urls import path, include
from api.views import index

urlpatterns = [
    path('', index, name='home'),
    path('api/', include('api.urls')),
]
