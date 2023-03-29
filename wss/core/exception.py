class ConnectionException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ConfigurationException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class AuthenticationException(ConnectionException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Unsupported authentication method: %s" % self.message