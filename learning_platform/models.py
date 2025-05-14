from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название образовательного курса",
    )
    description = models.TextField(
        verbose_name="Подробное описание курса",
        help_text="Опишите цели, программу и ожидаемые результаты курса",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор курса",
        related_name="created_courses"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        help_text="URL-идентификатор курса"
    )

    class Meta:
        verbose_name = "Образовательный курс"
        verbose_name_plural = "Образовательные курсы"
        ordering = ["-created_at", "name"]

    def __str__(self):
        return f"{self.name} (Автор: {self.owner.get_full_name() if self.owner else 'Не указан'})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def lessons_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
    )
    description = models.TextField(
        verbose_name="Содержание урока",
        help_text="Опишите материалы и задания урока",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        verbose_name="Входит в курс",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="lessons",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Преподаватель",
        related_name="created_lessons"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок в курсе"
    )

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"
        ordering = ["course", "order", "name"]
        permissions = [
            ("view_lesson_content", "Может просматривать содержание урока"),
            ("submit_lesson_work", "Может отправлять работы по уроку"),
        ]

    def __str__(self):
        course_name = f" ({self.course.name})" if self.course else ""
        return f"{self.name}{course_name}" 