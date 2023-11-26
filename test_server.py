import asyncio

from SlowAPI import SlowAPI


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