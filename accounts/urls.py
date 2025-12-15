from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterAPI,
    LoginAPI,
    LogoutAPI,
    ProfileAPI,

    RequestCreateAPI,
    RequestListAPI,
    RequestDetailAPI,

    ReviewCreateAPI,
    ReviewListAPI,
    ReviewDetailAPI,

    CategoryViewSet,
    ServiceViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"services", ServiceViewSet, basename="service")

urlpatterns = [
    # AUTH
    path("register/", RegisterAPI.as_view(), name="api-register"),
    path("login/", LoginAPI.as_view(), name="api-login"),
    path("logout/", LogoutAPI.as_view(), name="api-logout"),
    path("profile/", ProfileAPI.as_view(), name="api-profile"),

    # REQUESTS
    path("requests/", RequestListAPI.as_view(), name="request-list"),
    path("requests/create/", RequestCreateAPI.as_view(), name="request-create"),
    path("requests/<int:pk>/", RequestDetailAPI.as_view(), name="request-detail"),

    # REVIEWS
    path("reviews/", ReviewListAPI.as_view(), name="review-list"),
    path("reviews/create/", ReviewCreateAPI.as_view(), name="review-create"),
    path("reviews/<int:pk>/", ReviewDetailAPI.as_view(), name="review-detail"),

    # ROUTER (Categories & Services)
    path("", include(router.urls)),
]

