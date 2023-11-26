import asyncio

from request import Request
from response import Response


class SlowAPI:
    def __init__(self):
        self.routes = {'get': {}, 'post': {}}

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
        ret = await self.routes[request.method][request.path]()
        Response(ret, writer)

    async def run_server(self, host, port):
        server = await asyncio.start_server(
            self.handle_request, host, port
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()


app = SlowAPI()


@app.route('/', method='GET')
async def home(request):
    pass


@app.route('/hui', method='GET')
async def greet(request):
    pass


async def main():
    await app.run_server('127.0.0.1', 8080)

if __name__ == '__main__':
    asyncio.run(main())
