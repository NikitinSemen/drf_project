from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="materials/image", **NULLABLE, verbose_name="картинка"
    )

    owner = models.ForeignKey(
        "users.User", verbose_name="владелец", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(
        upload_to="materials/lesson/image", **NULLABLE, verbose_name="картинка"
    )
    url_video = models.URLField(**NULLABLE, verbose_name="ссылка на видео")
    course = models.ForeignKey(
        Course, verbose_name="курс", on_delete=models.SET_NULL, **NULLABLE
    )
    owner = models.ForeignKey(
        "users.User", verbose_name="владелец", on_delete=models.SET_NULL, **NULLABLE
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
