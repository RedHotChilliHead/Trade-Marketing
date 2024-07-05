from django.urls import path
from .views import EventApiView

app_name = "apistatisticapp"

urlpatterns = [
    path('', EventApiView.as_view(), name='events'),
]
