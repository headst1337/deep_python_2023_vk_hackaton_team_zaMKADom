import asyncio

from SlowAPI import SlowAPI


app = SlowAPI()


@app.get("/")
async def home(req):
    with open('templates/hello.html', 'r') as file:
        html = file.read()
    return html


@app.get("/cats")
async def cats(req):
    return "<h1>We love cats</h1>"


if __name__ == "__main__":
    app.run()
