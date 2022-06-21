import threading


class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()