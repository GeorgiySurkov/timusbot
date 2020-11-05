from telegram_handler.formatters import HtmlFormatter
from telegram_handler.utils import escape_html


class MyHtmlFormatter(HtmlFormatter):
    def format(self, record):
        s = super(MyHtmlFormatter, self).format(record)
        if record.exc_info:
            s += '\n' + self.formatException(record.exc_info)
        return s

    def formatException(self, *args, **kwargs):
        s = super(HtmlFormatter, self).formatException(*args, **kwargs)
        return f"<pre>{escape_html(s)}</pre>"
