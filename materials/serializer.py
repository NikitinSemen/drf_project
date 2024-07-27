from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import validate_urls
from users.models import Subscription


class CourseSerializer(ModelSerializer):
    lessons = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    def get_lessons(self, instance):
        return [lesson.name for lesson in Lesson.objects.filter(course=instance)]

    class Meta:
        model = Course
        fields = ('name', 'description', 'owner', 'lessons', 'is_subscribed')


class CourseDetailSerializer(ModelSerializer):
    count_lesson = SerializerMethodField()

    def get_count_lesson(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'count_lesson')


class LessonSerializer(ModelSerializer):
    url_video = CharField(validators=[validate_urls])

    class Meta:
        model = Lesson
        fields = ('name', 'description', 'course', 'url_video', 'owner')
