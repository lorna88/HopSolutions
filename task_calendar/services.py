import datetime


class DateProvider:
    """
    Manages access to the date. Issues the date given by filter.
    If this date is not specified provides a current date.
    """
    def __init__(self, date: str = None):
        """Save the date or get the current date."""
        if date:
            self.task_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            self.task_date = datetime.date.today()

    def get_date(self) -> datetime.date:
        """Gives the stored date"""
        return self.task_date
