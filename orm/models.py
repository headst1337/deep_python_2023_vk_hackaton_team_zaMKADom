from collections import OrderedDict
from manager import Manager


class Field:
    pass


class IntegerField(Field):
    pass


class CharField(Field):
    pass


class ModelMeta(type):

    def __new__(mcs, class_name, parents, attributes):
        fields = OrderedDict()
        for k, v in attributes.items():
            if isinstance(v, Field):
                fields[k] = v
                attributes[k] = None
        model = super(ModelMeta, mcs).__new__(mcs, class_name, parents, attributes)
        setattr(model, '_model_name', attributes['__qualname__'].lower())
        setattr(model, '_original_fields', fields)
        setattr(model, 'objects', Manager(model))
        return model


class Model(metaclass=ModelMeta):
    pass


class CityModel(Model):

    id = IntegerField()
    name = CharField()
    population = IntegerField()

    def __str__(self):
        return f'<City {self.id} : {self.name} population {self.population}>'

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    model = CityModel()
    print(model.id, model.name, model._model_name, model._original_fields)
    print(model.objects.filter(id=1).fetch())