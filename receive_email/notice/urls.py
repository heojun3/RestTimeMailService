from .views import NoticeViewSet
from django.urls import include, path
from rest_framework import routers
from . import views

# Router 설정
router = routers.DefaultRouter()
router.register(r'notices', NoticeViewSet)

# URL 패턴 설정
urlpatterns = [
    path('', views.index),
    path('api/', include(router.urls)),
]
