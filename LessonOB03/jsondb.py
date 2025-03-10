
import os
import json

class OopsError(Exception):
    pass


class JsonDb:

    def __init__(self, path=None, filename=None):
        self.path = path
        if not self.path:
            s_path, _ = os.path.split(__file__)
            self.path = s_path

        if not os.path.isdir(self.path):
            raise OopsError(f"Не удается открыть папку {self.path}")

        self.filename = filename if filename else "json-db.json"
        self.fullname = os.path.join(self.path, self.filename)
        self._data = {}
        self.indent = 3


    def write_data(self, dt):
        with open(self.fullname, 'w', encoding='utf-8') as f:
            json.dump(dt, f, ensure_ascii=False, indent=self.indent)


    def load_data(self):
        data = []
        if os.path.isfile(self.fullname):
            with open(self.fullname, 'r', encoding='utf-8') as f:
                data = json.load(f)
        return data
