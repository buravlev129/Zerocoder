

class Task:
    """
    Представляет задачу
    """

    _tags = {"New": "tg_new", "In work": "tg_work", "Done": "tg_done"}

    @staticmethod
    def get_supported_status_list():
        """
        Возвращает список статусов, которые поддерживает задача
        """
        return ["New", "In work", "Done"]

    @classmethod
    def from_array(cls, row):
        t = cls(row[0], row[1], row[2], row[3])
        return t

    def __init__(self, id=0, name="", description="", status=""):
        self.id = id
        self.name = name
        self.description = description
        self.status = status

    def get_tuple(self):
        return (self.id, self.name, self.description, self.status)
    
    @property
    def tag(self):
        if self.status in self._tags:
            return self._tags[self.status]
        return "tg_new"
        
    def __repr__(self):
        return f"{self.name} {self.status}"
    def __str__(self):
        return f"{self.name} {self.status}"
