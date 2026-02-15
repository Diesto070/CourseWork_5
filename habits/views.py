from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

from habits.models import Habit
from habits.paginations import HabitPagination
from habits.serializers import HabitSerializer, PublicHabitSerializer
from users.permissions import IsOwner


class HabitCreateAPIView(CreateAPIView):
    """Контроллер создания привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """Запись пользователя в качестве автора привычки."""
        serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    """Контроллер получения списка всех своих привычек."""

    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)
    pagination_class = HabitPagination

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    """Контроллер получения информации о конкретной привычке."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(UpdateAPIView):
    """Контроллер обновления информации о привычке."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class HabitDestroyAPIView(DestroyAPIView):
    """Контроллер удаления привычки."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class PublicHabitListAPIView(ListAPIView):
    """Контроллер получения списка всех публичных привычек."""

    queryset = Habit.objects.filter(is_published=True)
    serializer_class = PublicHabitSerializer
    permission_classes = []  # Доступно всем, даже без авторизации
    pagination_class = HabitPagination
