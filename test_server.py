import asyncio

from SlowAPI import SlowAPI


app = SlowAPI()


@app.get("/")
async def home():
    return "Hello, World!"


@app.get("/cats")
async def cats():
    return "We love cats"


if __name__ == "__main__":
    app.run()
