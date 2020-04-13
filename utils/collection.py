

class Collection:
    def __init__(self, array):
        self.array = array

    # Collection([A(x=1), A(x=2)]).index_by('x')  =>  {"1": A(x=1), "2": A(x=2)}
    def index_by(self, key):
        if not key:
            return {}
        indexed = {}
        for item in self.array:
            if hasattr(item, key):
                indexed[str(item.__getattribute__(key))] = item
        return indexed

    def find_all(self, **kwargs):
        return list(self._evaluator(kwargs))

    def find_one(self, **kwargs):
        return next(self._evaluator(kwargs), None)

    def _evaluator(self, d):
        for item in self.array:
            test = False
            for key in d.keys():
                test = True if hasattr(item, key) and item.__getattribute__(key) == d[key] else False
            if test:
                yield item


class A:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


if __name__ == '__main__':
    print(Collection([A(x=1), A(x=2)]).index_by('x'))