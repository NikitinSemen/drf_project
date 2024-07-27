from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateApiView, PaymentDestroyApiView,
                         PaymentListApiView, PaymentRetrieveApiView,
                         PaymentUpdateApiView, UserCreateApiView, SubscriptionView)

app_name = UsersConfig.name

urlpatterns = [
    path("payment/", PaymentListApiView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateApiView.as_view(), name="payment_create"),
    path(
        "payment/<int:pk>/", PaymentRetrieveApiView.as_view(), name="payment_retrieve"
    ),
    path(
        "payment/<int:pk>/delete",
        PaymentDestroyApiView.as_view(),
        name="payment_delete",
    ),
    path(
        "payment/<int:pk>/update", PaymentUpdateApiView.as_view(), name="payment_update"
    ),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe')
]
