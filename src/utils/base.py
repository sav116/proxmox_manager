from utils.logger_base import logger_decorator

class BaseMeta(type):

    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                attrs[attr_name] = logger_decorator(attr_value)
        return super().__new__(cls, name, bases, attrs)
