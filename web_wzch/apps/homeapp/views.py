from rest_framework.generics import ListAPIView

from homeapp.models import Banner, Nav
from homeapp.serializer import BannerModelSerializer, NavModelSerializer


# 轮播图接口
class BannerAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = BannerModelSerializer


# 导航栏头部接口
class HeaderAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True,position=1, is_delete=False).order_by("-orders")
    serializer_class = NavModelSerializer

# 导航栏底部接口
class FooterAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True,position=2, is_delete=False).order_by("-orders")
    serializer_class = NavModelSerializer