from django.urls import path

from cartapp import views

urlpatterns = [
    path("option/", views.CartViewSet.as_view({"post":"add_cart",
                                               "get":"list_cart",
                                               "put":"put",
                                               "delete":"delete",
                                               })),
]
