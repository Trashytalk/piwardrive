class DummyEvent:
    def cancel(self):
        pass


class Clock:
    @staticmethod
    def schedule_interval(callback, interval):
        return DummyEvent()

    @staticmethod
    def schedule_once(callback, timeout=0):
        return DummyEvent()

    @staticmethod
    def create_trigger(callback, timeout=0, interval=True):
        def trigger(*args, **kwargs):
            return callback(*args, **kwargs)
        return trigger

    @staticmethod
    def unschedule(ev):
        pass


def mainthread(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
