from SlowAPI import SlowAPI
from SlowAPI import Render


app = SlowAPI()


@app.get("/")
async def home():
    return Render().render('hello.html')

@app.get("/hello")
async def hello(name):
    return f"Hello: {name}"

@app.post("/cats")
async def cats(say):
    return f"We love cats: {say}"

@app.post("/user")
async def user(id, name):
    return f"User: id is {id} and name is: {name}"


if __name__ == "__main__":
    app.run()
