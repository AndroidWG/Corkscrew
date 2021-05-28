class ClientError(Exception):
    """Thrown when a HTTP request gets a response with a status code of 4xx"""

    def __init__(self, status_code, message="The server returned a client error status code."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"The server returned a client error status code: {self.status_code}."


class ServerError(Exception):
    """Thrown when a HTTP request gets a response with a status code of 5xx"""

    def __init__(self, status_code, message="The server returned a server error status code."):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"The server returned a server error status code: {self.status_code}."

