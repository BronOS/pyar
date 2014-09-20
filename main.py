from pyar.base import PyAR

class A(object):
    def __init__(self, **kwargs):
        self._test = dict()
        for key, value in kwargs.items():
            self._test[key] = value

        print(self._test)


a = A(xxx='ddd', r='ttt')
