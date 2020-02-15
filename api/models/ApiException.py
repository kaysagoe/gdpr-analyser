import pytz
from datetime import datetime


class ApiException(Exception):
    status_code = 400

    def __init__(self, error, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.error = error

    def to_dict(self):
        london = pytz.timezone("Europe/London")
        return {
            "timestamp": datetime.now(london).strftime("%d-%m-%YT%H:%M:%S"),
            "status": self.status_code,
            "error": self.error,
            "message": self.message
        }
