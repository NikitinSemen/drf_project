from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from .tasks import send_email_task

from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.pagination import CustomPagination
from materials.serializer import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
)
from materials.services import create_product_for_payment
from users.models import Payment, Subscription
from users.permissions import IsModer, IsOwner
from users.serializer import PaymentSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Просмотр списка курсов с пагинацией"))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание курса"))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Просмотр деталей курса"))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Редактирование курса"))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление курса"))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer

        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsAuthenticated,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.send_notifications(instance)
        return Response(serializer.data)

    def send_notifications(self, course):
        subscriptions = Subscription.objects.filter(course=course)
        for subscription in subscriptions:
            user = subscription.user
            self.send_notification(user, course)

    def send_notification(self, user, course):
        subject = f'Курс "{course.name}" обновлён'
        message = f'Курс "{course.name}" был обновлён. Пожалуйста, проверьте изменения.'
        from_email = EMAIL_HOST_USER
        
        send_email_task.delay(subject, message, from_email, [user.email])


class LessonCreateApiView(CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson_like_product_for_stripe = create_product_for_payment(lesson)
        lesson.product_id = lesson_like_product_for_stripe.get('id')

        lesson.save()


class LessonListApiView(ListAPIView):
    """Просмотр списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """Просмотр деталей одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    """Изменение урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)
