from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        reward = attrs.get("reward")
        related_habit = attrs.get("related_habit")
        action_time = attrs.get("action_time")
        is_pleasant = attrs.get("is_pleasant", False)
        periodicity = attrs.get("periodicity", 1)

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указать вознаграждение и связанную привычку."
            )

        if action_time is not None and action_time > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд."
            )

        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        if periodicity > 7:
            raise serializers.ValidationError(
                "Привычка должна выполняться хотя бы один раз в 7 дней."
            )

        return attrs

    class Meta:
        model = Habit
        fields = [
            "id",
            "place",
            "time",
            "action",
            "periodicity",
            "reward",
            "action_time",
            "public",
            "is_pleasant",
            "related_habit",
        ]

