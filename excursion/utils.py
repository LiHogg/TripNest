from datetime import datetime, timedelta, date
from .models import Excursion, ExcursionAvailability

def generate_excursion_schedule(excursion, start_date, end_date, start_time_str, max_time_str='20:00'):
    """
    Генерация расписания экскурсий по дням и времени.
    :param excursion: объект Excursion
    :param start_date: дата начала (datetime.date)
    :param end_date: дата окончания (datetime.date)
    :param start_time_str: строка, например '10:00'
    :param max_time_str: строка, например '20:00'
    """

    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    max_time = datetime.strptime(max_time_str, '%H:%M').time()

    # Длительность экскурсии в минутах + 20 минут
    duration_minutes = int(float(excursion.duration_hours) * 60) + 20
    duration = timedelta(minutes=duration_minutes)

    current_date = start_date

    while current_date <= end_date:
        current_time = datetime.combine(current_date, start_time)

        while current_time.time() <= max_time:
            ExcursionAvailability.objects.get_or_create(
                excursion=excursion,
                available_date=current_date,
                start_time=current_time.time(),
                defaults={'available_slots': excursion.max_participants}
            )
            current_time += duration

        current_date += timedelta(days=1)
