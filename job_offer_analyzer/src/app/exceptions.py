class ResponseStatusError(ValueError):
    def __init__(self, status):
        self.status = status