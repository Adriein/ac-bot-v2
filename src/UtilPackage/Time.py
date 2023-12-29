from datetime import datetime


class Time:
    @staticmethod
    def now():
        return datetime.now().astimezone().strftime("%d %b %Y, %H:%M:%S")
