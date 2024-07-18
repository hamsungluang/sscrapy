from copy import deepcopy
from importlib import import_module
from ssscrapy.settings import default_settings
from collections.abc import MutableMapping


class SettingsManager(MutableMapping):

    def __init__(self, values=None):
        self.attributes = {}
        self.set_settings(default_settings)
        self.update_values(values)

    def __getitem__(self, item):
        if item not in self:
            return None
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, item):
        return item in self.attributes

    def set(self, key, value):
        self.attributes[key] = value

    def get(self, name, default=None):
        return self[name] if self[name] is not None else default

    def getint(self, name, default=0):
        return int(self.get(name, default))

    def getfloat(self, name, default=0.0):
        return float(self.get(name, default))

    def getbool(self, name, default=False):
        got = self.get(name, default)
        try:
            return bool(int(got))
        except ValueError:
            if got in ('true', 'TRUE', 'True'):
                return True
            if got in ('false', 'FALSE', 'False'):
                return False
            raise ValueError("Support values for bool settings atr (0 or 1), (True or False)")

    def getlist(self, name, default=None):
        value = self.get(name, default or [])
        if isinstance(value, str):
            value = value.split(', ')
        return list(value)

    def __delitem__(self, key):
        self.delete(key)

    def delete(self, key):
        del self.attributes[key]

    def set_settings(self, module):
        if isinstance(module, str):
            module = import_module(module)
        for key in dir(module):
            if key.isupper():
                self.set(key, getattr(module, key))

    def __str__(self):
        return f"<Settings values={self.attributes}>"

    def update_values(self, values):
        if values is not None:
            for key, value in values.items():
                self.set(key, value)

    __repr__ = __str__

    def __iter__(self):
        return iter(self.attributes)

    def __len__(self):
        return len(self.attributes)

    def copy(self):
        return deepcopy(self)
