from django.contrib.auth import get_user_model
# from rest_framework import generics
from rest_framework import viewsets

from .serializers import CurrentUserSerializer, UserPostSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CurrentUserSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST'):
            return UserPostSerializer
        return CurrentUserSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()

#     def get_serializer_class(self):
#         if self.request.method in ('POST'):
#             return UserPostSerializer
#         return CurrentUserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = CurrentUserSerializer


# class UserCreate(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserPostSerializer
