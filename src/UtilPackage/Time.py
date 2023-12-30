from datetime import datetime, timedelta


class Time:
    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def format(date_time: datetime) -> str:
        return date_time.astimezone().strftime("%d %b %Y, %H:%M:%S")

    @staticmethod
    def add_minutes(date: datetime, minutes: int) -> datetime:
        delta = timedelta(minutes=minutes)

        return date + delta
