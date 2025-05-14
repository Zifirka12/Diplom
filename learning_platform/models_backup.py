class Test(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name="Урок"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название теста"
    )
    description = models.TextField(
        verbose_name="Описание теста",
        help_text="Укажите цель теста и инструкции по его прохождению",
        blank=True,
        null=True
    )
    passing_score = models.PositiveIntegerField(
        default=70,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Проходной балл (%)",
        help_text="Процент правильных ответов для успешного прохождения теста"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление"
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.lesson.name})"


class Question(models.Model):
    QUESTION_TYPES = (
        ('single', 'Один правильный ответ'),
        ('multiple', 'Несколько правильных ответов'),
        ('text', 'Текстовый ответ'),
    )

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Тест"
    )
    text = models.TextField(
        verbose_name="Текст вопроса"
    )
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='single',
        verbose_name="Тип вопроса"
    )
    points = models.PositiveIntegerField(
        default=1,
        verbose_name="Баллы за вопрос"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок вопроса"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["test", "order"]

    def __str__(self):
        return f"Вопрос {self.order} - {self.text[:50]}..."


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос"
    )
    text = models.TextField(
        verbose_name="Текст ответа"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Правильный ответ"
    )
    explanation = models.TextField(
        verbose_name="Объяснение",
        help_text="Объяснение, почему этот ответ правильный/неправильный",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return f"{self.text[:50]}... ({'✓' if self.is_correct else '✗'})"


class TestAttempt(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name="Тест"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name='test_attempts',
        verbose_name="Студент"
    )
    score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Результат (%)"
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Начало прохождения"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Завершение"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Завершен"
    ) 