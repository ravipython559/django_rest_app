from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    TodoListApiView,
    TodoDetailApiView
)

urlpatterns = [
    path('api', TodoListApiView.as_view(), name='api'),
    path('api/<int:todo_id>/', TodoDetailApiView.as_view(), name='api_details'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]