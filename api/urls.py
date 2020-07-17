from django.urls import path
from api import views


app_name = 'api'


urlpatterns = [
    path('start/', views.Start.as_view(), name='start'),
    path('state/', views.GetState.as_view(), name='state'),
]
