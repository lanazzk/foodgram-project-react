from django.urls import include, path

from .views import UserDetail, UserList

app_name = 'users'


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('', include('djoser.urls')),
]
