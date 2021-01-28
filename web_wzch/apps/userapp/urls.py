from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from userapp import views

urlpatterns = [
    # 借助于jwt完成登录请求
    path("login/", obtain_jwt_token),
    path("captcha/", views.CaptchaAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
    path("message/", views.MessageAPIView.as_view()),
]
