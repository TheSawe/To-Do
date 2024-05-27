import datetime
from app.functionality.storage import weekdays, months


def get_current_date():
    today = datetime.date.today()
    return f'{weekdays[datetime.date.weekday(today)]}, {str(today)[8:11]} {months[str(str(today)[5:7])]}'