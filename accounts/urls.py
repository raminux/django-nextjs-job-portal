from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('token/', TokenObtainPairView.as_view()), 
    path('token/verify/', TokenVerifyView.as_view()),
    path('me/', views.current_user, name='current_user'),
    path('me/update/', views.update_user, name='update_user')

]