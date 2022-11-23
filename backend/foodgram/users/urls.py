from django.urls import include, path

# from .views import UserDetail, UserList

app_name = 'users'


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
