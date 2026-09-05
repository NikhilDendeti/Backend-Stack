import json
import os

class BookNotAvailableError(Exception):
    pass

class LibraryItem:
    def __init__(self,item_id,name):
        self.item_id=item_id
        self.name=name

        def __str__(self):
            return f"[{self.item_id}] {self.name}"

class Person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

    def __str__(self):
        return f"{self.name} (ID: {self.person_id})"

class Book(LibraryItem):
    def __init__(self, item_id, title, author, available=True):
        super().__init__(item_id, title)         
        self.author = author
        self.available = available
 
    def __str__(self):
        status = "available" if self.available else "borrowed"
        base = super().__str__()                 
        return f"{base} by {self.author} — {status}"
 
    def to_dict(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "author": self.author,
            "available": self.available,
        }
 
    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data["item_id"],
            title=data["title"],
            author=data["author"],
            available=data["available"],
        )

