

class User:
    """
    Пользователь
    """
    def __init__(self, user_id, name):
        self._user_id = user_id
        self._name = name
        self._access_level = 'user'

    @property
    def user_id(self):
        return self._user_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def access_level(self):
        return self._access_level

    @property
    def is_admin(self):
        return self._access_level == "admin"



class Admin(User):
    """
    Администратор
    """
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self._access_level = 'admin'
        self._users = {}

    def add_user(self, user_id, name):
        if user_id in self._users:
            print(f"User with ID {user_id} already exists.")
        else:
            user = User(user_id, name)
            self._users[user_id] = user
            print(f"User {name} added successfully.")

    def remove_user(self, user_id):
        if user_id in self._users:
            del self._users[user_id]
            print(f"User with ID {user_id} removed successfully.")
        else:
            print(f"User with ID {user_id} does not exist.")

    @property
    def count(self):
        """Возвращает количество пользователей"""
        return len(self._users)

    def get_user(self, user_id):
        if user_id in self._users:
            return self._users[user_id]
        return None

    def get_all_users(self):
        return self._users





if __name__ == "__main__":

    admin = Admin(0, "Admin")
    admin.add_user(1, "Alice")
    admin.add_user(2, "Bob")
    assert admin.is_admin

    user1 = admin.get_user(2)
    assert user1.name == "Bob"
    assert user1.access_level == "user"
    assert not user1.is_admin

    user1.name = "John"
    user1 = admin.get_user(2)
    assert user1.name == "John"

    print(f"Количество пользователей: {admin.count}")

    admin.remove_user(2)
    print(f"Количество пользователей: {admin.count}")
    assert admin.get_user(2) is None
    assert admin.count == 1
