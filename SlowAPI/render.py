import os


class Render:

    def __init__(self, path='/templates/'):
        self.path = os.getcwd() + path

    def render(self, name, **kwargs):
        print(self.path + name)
        with open(self.path + name, 'r') as file:
            html = file.read()
            for key, value in kwargs.items():
                html = html.replace(f'{{{key}}}', value)
            return html
