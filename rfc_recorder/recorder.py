from collections import namedtuple
from functools import wraps


RecordKey = namedtuple('RecordKey', 'function_name args kwargs')


class Recorder(object):
    """Record connection activity and save it for future replay

    This is intented to be used on tests.
    Is assumed that function calls are idempotent

    Usage
    -----
    Context Manager
    Decorator

    """

    def __init__(self, connection, record=True):
        """Initialize a new Recorder

        :param connection: a ``pyrfc.Connection`` object.
        """
        self.records = {}
        self.record = record

    def __enter__(self):
        """Load records if they exists"""
        return self

    def __exit__(self, *_):
        """Clean resources on context exit

        save new records on disk
        """


    def _record_decorator(self, f):
        """Decorates a function with recording behaviour

        :param f: any callable
        """

        @wraps(f)
        def wrapper(*args, **kwargs):
            key = RecordKey(f.__name__, args, kwargs)

            if key not in self.records:
                result = f(*args, **kwargs)
                if self.record:
                    self.records[key] = result
                return result

            return self.records[key]

        return wrapper
