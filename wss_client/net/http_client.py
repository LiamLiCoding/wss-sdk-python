import time


class AsyncHttpClient:
    def __init__(self, device_key):
        self.m_device_key = device_key

    @staticmethod
    def get_timestamp():
        millis = int(round(time.time() * 1000))
        return millis

    # TODO: HTTP client is still developing
    def send(self):
        pass
