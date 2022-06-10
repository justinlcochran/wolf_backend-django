from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MyTokenObtainPairView, main, rollChange

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('main/<int:pk>/', main, name='main'),
    path('rollChange/', rollChange, name='rollChange')
    ]