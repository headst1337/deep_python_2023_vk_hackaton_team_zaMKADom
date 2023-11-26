import asyncio

from SlowAPI import SlowAPI
from SlowAPI import Render


app = SlowAPI()


@app.get("/")
async def home():
    return Render().render('hello.html')


@app.get("/cats")
async def cats(cat_id=None):
    if cat_id is None:
        return "<h1>We love cats</h1>"
    return f"<h1>We love cats with cat_id:{cat_id}</h1>"


if __name__ == "__main__":
    app.run()
