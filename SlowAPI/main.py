import asyncio

from SlowAPI.request import Request
from SlowAPI.response import Response
from SlowAPI.slowserver import SlowServer


class SlowAPI:
    def __init__(self):
        self.routes = {"GET": {}, "POST": {}}
        self.ip = "127.0.0.1"
        self.port = 8080

    def set_ip(self, ip, port):
        self.ip = ip
        self.port = port

    def get(self, path):
        def wrapper(handler):
            self.routes["GET"][path] = handler
            return handler

        return wrapper

    def post(self, path):
        def wrapper(handler):
            self.routes["POST"][path] = handler
            return handler

        return wrapper

    async def handle_request(self, reader, writer):
        request = Request(await reader.read(10000))

        try:
            body = await self.routes[request.method][request.path](request)
            print("b", body)
        except Exception as e:
            resp = Response(status_code=404, status_message="Not Found", body=str(e))
        else:
            resp = Response(status_code=200, status_message="OK", body=body)
        finally:
            print("r", resp)
            await resp.send(writer)

    def run(self):
        serv = SlowServer(self.handle_request)
        asyncio.run(serv.run_server(self.ip, self.port))
