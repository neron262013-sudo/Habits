from celery import shared_task
from django.utils import timezone

from habits.models import Habit


@shared_task
def check_habits():
    now = timezone.localtime()
    today = now.date()

    habits = Habit.objects.filter(
        time__hour=now.hour,
        time__minute=now.minute,
    )

    for habit in habits:
        days_passed = (today - habit.created_at.date()).days

        if days_passed % habit.periodicity == 0:
            print(
                f"Пора выполнить: {habit.action}. "
                f"Пользователь: {habit.user}"
            )