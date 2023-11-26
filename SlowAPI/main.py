import asyncio

from SlowAPI.request import Request
from SlowAPI.response import Response


class SlowAPI:
    def __init__(self):
        self.routes = {'GET': {}, 'POST': {}}

    def get(self, path):
        def wrapper(handler):
            self.routes['GET'][path] = handler
            return handler
        return wrapper

    def post(self, path):
        def wrapper(handler):
            self.routes['POST'][path] = handler
            return handler
        return wrapper

    async def handle_request(self, reader, writer):
        request = Request(await reader.read(10000))

        try:
            body = await self.routes[request.method][request.path]()
            Response(status_code=200, status_message='OK', body=body).send(writer)
        except Exception as e:
            body = str(e)
            Response(status_code=404, status_message='Not Found', body=body).send(writer)

    async def run_server(self, host, port):
        server = await asyncio.start_server(
            self.handle_request, host, port
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
