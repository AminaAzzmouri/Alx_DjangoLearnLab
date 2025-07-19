from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None

def query_all_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None

def query_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian
        return librarian
    except Library.DoesNotExist:
        return None
    except Librarian.DoesNotExist:
        return None


# Example usage
if __name__ == "__main__":
    author_books = query_all_books_by_author("J.K. Rowling")
    print(f"Books by J.K. Rowling: {[book.title for book in author_books]}")

    library_books = query_all_books_in_library("Central Library")
    print(f"Books in Central Library: {[book.title for book in library_books]}")

    librarian = query_librarian_for_library("Central Library")
    if librarian:
        print(f"Librarian for Central Library: {librarian.name}")
    else:
        print("No librarian found for Central Library.")
