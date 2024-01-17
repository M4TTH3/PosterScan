from ics import Calendar, Event
from datetime import datetime, timedelta
import base64

def create_ical(title, date):
    c = Calendar()
    e = Event()
    e.name = title
    start_datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    e.begin = start_datetime
    e.end = start_datetime + timedelta(hours=24)
    c.events.add(e)

    with open('test.ics', 'w') as my_file:
        my_file.writelines(c.serialize_iter())

    with open('test.ics', 'rb') as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string
