from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserDetail, UserList

app_name = 'users'


urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'))
]
