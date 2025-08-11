from django.contrib import admin
from django.urls import include, path

from client.views import ClientViewSet, HistoricalViewSet, RegisterUser

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"client", ClientViewSet)
router.register(r"historical", HistoricalViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("admin/", admin.site.urls),
    path("api/register/", RegisterUser.as_view(), name='register_user'),
]
