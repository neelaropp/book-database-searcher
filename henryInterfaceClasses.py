# henryInterfaceClasses.py
class Author:
    def __init__(self, author_id, first_name, last_name):
        self.author_id = author_id
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publisher:
    def __init__(self, publisher_code, publisher_name):
        self.publisher_code = publisher_code
        self.publisher_name = publisher_name

    def __str__(self):
        return f"{self.publisher_name}"

class Category:
    def __init__(self, category_type):
        self.category_type = category_type

    def __str__(self):
        return self.category_type
