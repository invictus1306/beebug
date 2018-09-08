from crash_anal.signals import dangerous_signals


class Checks(object):
    @staticmethod
    def check_signal(signal):
        if signal in dangerous_signals:
            return True
        return False