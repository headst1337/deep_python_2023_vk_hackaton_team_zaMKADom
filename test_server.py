import asyncio

from SlowAPI import SlowAPI


app = SlowAPI()


@app.get('/')
async def home(request):
    return f"{request.method} \n {request.path} \n {request.protocol} \n {request.headers}"


@app.post('/post')
async def greet(request):
    return f"{request.method} \n {request.path} \n {request.protocol} \n {request.headers}"


if __name__ == '__main__':
    app.run()