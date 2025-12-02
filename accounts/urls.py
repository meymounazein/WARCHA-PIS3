from django.urls import path
from .views import RegisterAPI, LoginAPI, LogoutAPI, ProfileAPI

urlpatterns = [
    path("api/register/", RegisterAPI.as_view(), name="api-register"),
    path("api/login/", LoginAPI.as_view(), name="api-login"),
    path("api/logout/", LogoutAPI.as_view(), name="api-logout"),
    path("api/profile/", ProfileAPI.as_view(), name="api-profile"),
]
from .views import (
    RequestCreateAPI,
    RequestListAPI,
    RequestDetailAPI,
)

urlpatterns += [
    path("api/requests/create/", RequestCreateAPI.as_view()),
    path("api/requests/", RequestListAPI.as_view()),
    path("api/requests/<int:pk>/", RequestDetailAPI.as_view()),
]
from .views import (
    ReviewCreateAPI,
    ReviewListAPI,
    ReviewDetailAPI,
)

urlpatterns += [
    path("api/reviews/create/", ReviewCreateAPI.as_view()),
    path("api/reviews/", ReviewListAPI.as_view()),
    path("api/reviews/<int:pk>/", ReviewDetailAPI.as_view()),
]

