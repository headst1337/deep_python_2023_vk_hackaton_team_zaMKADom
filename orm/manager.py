from query import Query, OR
from connector import DBConnector


class Manager:

    def __init__(self, models_class):
        self.models_class = models_class
        self._model_fields = models_class._original_fields.keys()
        q = Query()
        self.q = q.SELECT(*self._model_fields).FROM(models_class._model_name)
        self._connector = DBConnector()

    def filter(self, **kwargs):
        self.q = self.q.WHERE(**kwargs)
        return self

    def fetch(self):
        q = str(self.q)
        db_results = self._connector.fetch(q)
        results = []
        for row in db_results:
            model = self.models_class()
            for field, val in zip(self._model_fields, row):
                setattr(model, field, val)
            results.append(model)
        return results
