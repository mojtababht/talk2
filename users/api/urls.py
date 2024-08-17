from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, UserViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UserViewSet)
