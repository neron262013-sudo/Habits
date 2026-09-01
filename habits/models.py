from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь привычки", help_text="Укажите пользователя привычки"
    )
    place = models.CharField(max_length=100, verbose_name="Место", help_text="Укажите место")
    time = models.TimeField(verbose_name="Время начала", help_text="Укажите когда будет выполняться привычка")
    action = models.TextField(verbose_name="Действие", help_text="Укажите что представляет собой привычка")
    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Периодичность",
        help_text="Укажите периодичность привычки",
    )
    reward = models.CharField(
        max_length=100, verbose_name="Вознаграждение", help_text="Укажите вознаграждение", blank=True, null=True
    )
    action_time = models.PositiveIntegerField(
        verbose_name="Время выполнения",
        help_text="Укажите время на выполнение привычки",
    )
    public = models.BooleanField(
        default=False,
        verbose_name="Публичность",
        help_text="Укажите публичная ли привычка",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Приятная привычка",
        help_text="Укажите приятная ли привычка",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Укажите связанную привычку",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.user} буду {self.action} в {self.time} в {self.place}"
