import datetime
import decimal
import json
from setuptools.compat import basestring


class Jsonable:
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            if isinstance(value, datetime.datetime):
                iso = value.isoformat()
                yield attr, iso
            elif isinstance(value, decimal.Decimal):
                yield attr, str(value)
            elif hasattr(value, '__iter__'):
                if hasattr(value, 'pop'):
                    a = []
                    for subval in value:
                        if hasattr(subval, '__iter__'):
                            a.append(dict(subval))
                        else:
                            a.append(subval)
                    yield attr, a
                else:
                    yield attr, dict(value)
            else:
                yield attr, value

    def to_json(self):
        """Represent instance of a class as JSON.
      Arguments:
      obj -- any object
      Return:
      String that represent JSON-encoded object.
      """
        def serialize(obj):
            """Recursively walk object's hierarchy."""
            if isinstance(obj, (bool, int, float, basestring)):
                return obj
            elif isinstance(obj, dict):
                obj = obj.copy()
                for key in obj:
                    obj[key] = serialize(obj[key])
                return obj
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(serialize([item for item in obj]))
            elif hasattr(obj, '__dict__'):
                return serialize(obj.__dict__)
            else:
                return repr(obj)  # Don't know how to handle, convert to string

        serialized = serialize(self)
        return serialized

