import asyncio

from SlowAPI import SlowAPI
from SlowAPI import Render


app = SlowAPI()


@app.get("/")
async def home():
    return Render().render('hello.html')


@app.get("/cats")
async def cats(cat_id=None):
    if not cat_id:
        return "We love cats"
    return f"<h1>We love cats with cat_id:{cat_id}</h1>"


if __name__ == "__main__":
    app.run()
