class BaseLogger(object):

    def log(self, message, **kwargs):
        pass

class CompositeLogger(BaseLogger):

    def __init__(self, loggers):
        for l in loggers: assert isinstance(l, BaseLogger)
        self.loggers = loggers

    def log(self, message, **kwargs):
        for l in self.loggers:
            l.log(message, **kwargs)
