import asyncio

from SlowAPI import SlowAPI


app = SlowAPI()


@app.get("/")
async def home():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
