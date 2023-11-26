import asyncio


class SlowServer:
    def __init__(self, handler):
        self.handler = handler

    async def run_server(self, host, port):
        server = await asyncio.start_server(
            self.handler, host, port
        )

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()