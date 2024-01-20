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

    @staticmethod
    def minutes_between(date1: datetime, date2: datetime) -> int:
        """
            Get difference between two dates in minutes

            Args:
                date1 (datetime): nearest date to now which means bigger date
                date2 (datetime): farthest date to current date which means smaller date

            Returns:
                int: minutes
            """
        delta = date1 - date2

        return int(round(delta.total_seconds() / 60, 0))

