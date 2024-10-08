
import os
import json
from apperrors import OopsError


class AppState:
    """
    Помогает сохранять и восстанавливать состояние приложения при закрытии и последующем открытии.\\
    Например, может хранить размеры и положение окна на экране
    """

    def __init__(self, path=None, filename=None):
        self.path = path
        if not self.path:
            s_path, _ = os.path.split(__file__)
            self.path = s_path

        if not os.path.isdir(self.path):
            raise OopsError(f"Не удается открыть папку {self.path}")

        self.filename = filename if filename else "appstate.json"
        self.fullname = os.path.join(self.path, self.filename)
        self._data = {}
        self.indent = 3


    def load(self):
        self._data = {}
        if not os.path.exists(self.fullname):
            return
        with open(self.fullname, 'r') as f:
            self._data = json.load(f)


    def save(self):
        with open(self.fullname, 'w') as f:
            json.dump(self._data, f, indent=self.indent)


    def get_value(self, key, defval=None):
        """
        Возвращает элемент из внутреннего словаря по указанному ключу. 
        """
        if not key:
            return defval

        keys = key.split(".")
        temp = self._data
        b_found = False

        def is_end_of_list(i):
            return i == len(keys) -1

        for i, k in enumerate(keys):
            k = k.strip()
            if k:
                if isinstance(temp, dict):
                    if k in temp:
                        temp = temp[k]
                        if not isinstance(temp, dict) or is_end_of_list(i):
                            b_found = True
                            break
                    else:
                        break

        return temp if b_found else defval


    def get_int(self, key, defval=None):
        val = self.get_value(key, defval)
        if val:
            return int(val)
        return defval


    @staticmethod
    def _split_keypath(path):
        array = path.split(".")
        key = array[len(array) - 1]
        path_list = [x for i, x in enumerate(array) if i < len(array) - 1]
        return path_list, key


    def set_value(self, path, value):
        """
        Добавляет элемент с указанным значением во внутренный словарь. 
        - path: name1.name2.name3
        - value: значение, добавляемое в словарь        
        """

        path_list, key = self._split_keypath(path)

        if not key:
            return False

        if not path_list:
            self._data[key] = value
            return True

        temp = self._data
        b_found = False

        def is_end_of_list(i):
            return i == len(path_list) -1

        for i, k in enumerate(path_list):
            k = k.strip()
            if not k:
                return False
            if not isinstance(temp, dict):
                return False

            if k in temp:
                temp = temp[k]
                if is_end_of_list(i):
                    if isinstance(temp, dict):
                        temp[key] = value
                        b_found = True
                    break
            else:
                temp[k] = {}
                temp = temp[k]
                if is_end_of_list(i):
                    temp[key] = value
                    b_found = True
                    break
        return b_found



def test_set_value():
    """
    Юнит-тесты метода set_value
    """
    st = AppState()
    st._data = {}
    st.set_value("Tracer", {"driver": "OLEDB", "timeout": 55})
    assert st._data == { "Tracer": {"driver": "OLEDB", "timeout": 55}}

    st.set_value("Tracer.driver", "ORACLE")
    assert st._data == { "Tracer": {"driver": "ORACLE", "timeout": 55}}

    st.set_value("Tracer.user", "Admin")
    st.set_value("Tracer.passwd", "kyky")
    assert st._data == { "Tracer": {"driver": "ORACLE", "timeout": 55, "user": "Admin", "passwd": "kyky"}}

    st.set_value("Connection.Database", "MyORAdb")
    assert st._data == { "Tracer": {"driver": "ORACLE", "timeout": 55, "user": "Admin", "passwd": "kyky"}, "Connection": { "Database": "MyORAdb" }}

    print("test_set_value - Ok")




if __name__ == "__main__":

    test_set_value()
    print("---")

