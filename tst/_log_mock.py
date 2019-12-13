class LogMock:
    last = None
    def __call__(self, log_entry):
        self.last = log_entry