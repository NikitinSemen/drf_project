from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lessons = SerializerMethodField()

    def get_lessons(self, instance):
        return [lesson.name for lesson in Lesson.objects.filter(course=instance)]

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    count_lesson = SerializerMethodField()

    def get_count_lesson(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'count_lesson')


class LessonSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ('name', 'description', 'course')
