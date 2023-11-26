# SlowAPI 🐌

SlowAPI - это асинхронный веб-фреймворк, написанный на Python 3.11, который позволяет создавать простые и быстрые веб-приложения с минимальным кодом.
Также имеется ORM с базовым функцианалом.

## Зависимости 📦

Python 3.11

## Примеры использования 🚀

Вот несколько примеров того, как вы можете использовать SlowAPI для создания веб-приложений:

### Простой роутинг

Вы можете определить различные пути для вашего приложения с помощью декораторов `@app.get` и `@app.post`. Вы также можете передавать параметры в функции, которые обрабатывают запросы.

```python
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
```

### Шаблонизация

Вы можете использовать рендеринг HTML-шаблонов с помощью класса `Render`. Просто создайте папку `templates` в корне вашего проекта и поместите туда ваши HTML-файлы. Затем вы можете вызвать метод `render` с именем файла и любыми переменными, которые вы хотите передать в шаблон.

```python
from SlowAPI import SlowAPI
from SlowAPI import Render


app = SlowAPI()


@app.get("/")
async def home():
    return Render().render('hello.html', name='World')
```

### Запуск приложения

Чтобы запустить ваше приложение, вам нужно импортировать класс `SlowAPI` и создать экземпляр приложения. Затем вы можете вызвать метод `run` с параметрами `host` и `port`. По умолчанию они равны `localhost` и `8080`.

```python
from SlowAPI import SlowAPI


app = SlowAPI()


# Определите ваши пути здесь


if __name__ == "__main__":
    app.run()
```
