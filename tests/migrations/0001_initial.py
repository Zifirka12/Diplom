# Generated by Django 5.0.14 on 2025-05-16 08:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('learning_platform', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
                ('question_type', models.CharField(choices=[('single', 'Один правильный ответ'), ('multiple', 'Несколько правильных ответов'), ('text', 'Текстовый ответ')], default='single', max_length=10, verbose_name='Тип вопроса')),
                ('points', models.PositiveIntegerField(default=1, verbose_name='Баллы за вопрос')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['test', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('explanation', models.TextField(blank=True, help_text='Объяснение, почему этот ответ правильный/неправильный', null=True, verbose_name='Объяснение')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tests.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название теста')),
                ('description', models.TextField(blank=True, help_text='Укажите цель теста и инструкции по его прохождению', null=True, verbose_name='Описание теста')),
                ('passing_score', models.PositiveIntegerField(default=70, help_text='Процент правильных ответов для успешного прохождения теста', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Проходной балл (%)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_tests', to='learning_platform.lesson', verbose_name='Урок')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tests.test', verbose_name='Тест'),
        ),
        migrations.CreateModel(
            name='TestAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Результат (%)')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='Начало прохождения')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Завершение')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Завершен')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='tests.test', verbose_name='Тест')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_attempts', to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Попытка прохождения теста',
                'verbose_name_plural': 'Попытки прохождения тестов',
                'ordering': ['-started_at'],
            },
        ),
    ]
