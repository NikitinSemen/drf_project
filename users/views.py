from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from users.models import Payment, User, Subscription
from users.serializer import PaymentSerializer, UserSerializer, SubscriptionSerializer
from users.services import create_price_for_payment, create_session_for_payment


class PaymentCreateApiView(CreateAPIView):
    """Создание платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        price = create_price_for_payment(payment.amount)
        session_id, link = create_session_for_payment(price)
        payment.session_id = session_id
        payment.link = link
        payment.save()


class PaymentListApiView(ListAPIView):
    """Просмотр списка платежей"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ("paid_lesson", "paid_course", "payment_type")
    ordering_fields = ("date_of_payment",)


class PaymentRetrieveApiView(RetrieveAPIView):
    """Просмотр деталей платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDestroyApiView(DestroyAPIView):
    """Удаление платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    """Редактирование платежа"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UserCreateApiView(CreateAPIView):
    """Создание Пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(
        request_body=SubscriptionSerializer,
        responses={201: SubscriptionSerializer},
        operation_description="Подписать пользователя на курс"
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            subscription = Subscription.objects.create(user=user, course=course_item)
            serializer = self.serializer_class(subscription)
            return Response(serializer.data, status=201)
