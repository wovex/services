import logging
import json


LOG = logging.getLogger('app')


class myFormattor(logging.Formatter):
    def usesTime(self):
        return True


class MyFileHandler(logging.handlers.RotatingFileHandler):
    def format(self, record):
        msg = super().format(record=record)
        s = {"filename": record.filename, "level": record.levelname,"created": record.asctime, "message": msg}
        return json.dumps(s)


def init_log():
    handler = MyFileHandler('/var/log/app.log', maxBytes=10000000, backupCount=3)
    formattor = myFormattor()
    handler.setFormatter(formattor)
    LOG.setLevel(logging.DEBUG)
    LOG.addHandler(handler)
