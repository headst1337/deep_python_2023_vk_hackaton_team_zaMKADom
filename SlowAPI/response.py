class Response:
    def __init__(self, status_code=200, status_message="OK", headers=None, body=None):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = headers or {}
        self.body = body or ""

    def set_header(self, key, value):
        self.headers[key] = value

    def set_body(self, body):
        self.body = body

    def build(self):
        return (
            f"HTTP/1.1 {self.status_code} {self.status_message}\r\n"
            + "\r\n".join([f"{key}: {value}" for key, value in self.headers.items()])
            + f"\r\n\r\n{self.body}"
        )

    async def send(self, writer):
        writer.write(self.build().encode())
        await writer.drain()
        writer.close()
