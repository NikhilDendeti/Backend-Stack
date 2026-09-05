import json
import os

DATA_FILE = "library.json"


class BookNotAvailableError(Exception):
    pass


class LibraryItem:
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title

    def __str__(self):
        return f"[{self.item_id}] {self.title}"

    def __repr__(self):
        return f"LibraryItem(item_id={self.item_id!r}, title={self.title!r})"


class Book(LibraryItem):
    def __init__(self, item_id, title, author, available=True):
        super().__init__(item_id, title)
        self.author = author
        self.available = available

    def __str__(self):
        if self.available:
            status = "available"
        else:
            status = "borrowed"
        return f"{super().__str__()} by {self.author} - {status}"

    def __repr__(self):
        return f"Book(item_id={self.item_id!r}, title={self.title!r}, author={self.author!r}, available={self.available!r})"

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


class Person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

    def __str__(self):
        return f"{self.name} (ID: {self.person_id})"

    def __repr__(self):
        return f"Person(person_id={self.person_id!r}, name={self.name!r})"


class Member(Person):
    def __init__(self, person_id, name, borrowed_items=None):
        super().__init__(person_id, name)
        if borrowed_items is None:
            self.borrowed_items = []
        else:
            self.borrowed_items = borrowed_items

    def __str__(self):
        return f"{super().__str__()} - {len(self.borrowed_items)} book(s) borrowed"

    def __repr__(self):
        return f"Member(person_id={self.person_id!r}, name={self.name!r}, borrowed_items={self.borrowed_items!r})"

    def to_dict(self):
        return {
            "person_id": self.person_id,
            "name": self.name,
            "borrowed_items": self.borrowed_items,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            person_id=data["person_id"],
            name=data["name"],
            borrowed_items=data["borrowed_items"],
        )


class Library:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.books = {}
        self.members = {}
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            print("library.json is corrupted, starting with empty library")
            return
        except FileNotFoundError:
            return
        else:
            for book_data in data.get("books", []):
                book = Book.from_dict(book_data)
                self.books[book.item_id] = book

            for member_data in data.get("members", []):
                member = Member.from_dict(member_data)
                self.members[member.person_id] = member
        finally:
            print(f"Loaded {len(self.books)} books and {len(self.members)} members")

    def save_data(self):
        books_list = []
        for book in self.books.values():
            books_list.append(book.to_dict())

        members_list = []
        for member in self.members.values():
            members_list.append(member.to_dict())

        data = {
            "books": books_list,
            "members": members_list,
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def add_book(self, item_id, title, author):
        if item_id in self.books:
            print("Book id already exists")
            return
        self.books[item_id] = Book(item_id, title, author)
        self.save_data()

    def add_member(self, person_id, name):
        if person_id in self.members:
            print("Member id already exists")
            return
        self.members[person_id] = Member(person_id, name)
        self.save_data()

    def borrow_book(self, item_id, person_id):
        try:
            book = self.books[item_id]
            member = self.members[person_id]
        except KeyError:
            print("Book id or member id does not exist")
            return

        try:
            if not book.available:
                raise BookNotAvailableError(f"'{book.title}' is already borrowed")
        except BookNotAvailableError as e:
            print(f"Cannot borrow: {e}")
        else:
            book.available = False
            member.borrowed_items.append(item_id)
            self.save_data()
            print(f"{member.name} borrowed '{book.title}'")

    def return_book(self, item_id, person_id):
        try:
            book = self.books[item_id]
            member = self.members[person_id]
        except KeyError:
            print("Book id or member id does not exist")
            return

        if item_id not in member.borrowed_items:
            print(f"{member.name} did not borrow this book")
            return

        book.available = True
        member.borrowed_items.remove(item_id)
        self.save_data()
        print(f"{member.name} returned '{book.title}'")

    def list_books(self):
        if not self.books:
            print("No books in library")
            return
        for book in self.books.values():
            print(book)

    def list_members(self):
        if not self.members:
            print("No members in library")
            return
        for member in self.members.values():
            print(member)


def print_menu():
    print("\n--- Library Management ---")
    print("1. Add book")
    print("2. Add member")
    print("3. Borrow book")
    print("4. Return book")
    print("5. List books")
    print("6. List members")
    print("7. Exit")


def main():
    library = Library()

    while True:
        print_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            item_id = input("Book id: ")
            title = input("Title: ")
            author = input("Author: ")
            library.add_book(item_id, title, author)

        elif choice == "2":
            person_id = input("Member id: ")
            name = input("Name: ")
            library.add_member(person_id, name)

        elif choice == "3":
            item_id = input("Book id: ")
            person_id = input("Member id: ")
            library.borrow_book(item_id, person_id)

        elif choice == "4":
            item_id = input("Book id: ")
            person_id = input("Member id: ")
            library.return_book(item_id, person_id)

        elif choice == "5":
            library.list_books()

        elif choice == "6":
            library.list_members()

        elif choice == "7":
            print("Bye")
            break

        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
