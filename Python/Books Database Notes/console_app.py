import books_ratings
import connect_books
import tabulate
import connect_books as cb
import books_ratings as br
import psycopg2 as pg
import Books

def menu() -> str:
    """
    Present a menu to the user and return a valid option
    :return: 1, 2, Q, q
    """

    while True:
        print("1) Look up book by ISBN")
        print("2) Look up book by author")
        print("3) Find an author's avg book rating")
        print("4) Find the avg rating for the book by title and author")
        print("5) Find the avg rating for the user with the most reviews")
        print("6) Insert a new user")
        print("7) Insert a book")
        print("8) Insert a new review")
        print("9) Find the top n authors based on number of books published")
        print("10) List the top n books")
        print("Q) Quit")
        opt = input("> ")
        if opt in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'q']:
            return opt


if __name__ == "__main__":
    conn = connect_books.connect()
    books = Books.Books(conn)
    while True:
        opt = menu()
        if opt == '1':
            isbn = input("Enter an ISBN: ")
            conn = connect_books.connect()
            print(books_ratings.get_title_by_isbn(conn, isbn))
            # get title by ISBN
        elif opt == '2':
            author = input("Enter an author: ")

            print(tabulate.tabulate(books.get_books_by_author(conn, author),
                                    headers = ["Title", "Year", "Publisher", "ISBN"],
                                    tablefmt= "fancy_outline"))
            # get books by author
        elif opt in ['Q','q']:
            break
        elif opt == '3':
            author = input("Enter an author: ")
            conn = connect_books.connect()
            print(tabulate.tabulate(books_ratings.avg_rating_by_author(conn, author)))
        elif opt == '4':
            author = input("Enter the author: ")
            book = input("Enter a book: ")
            conn = connect_books.connect()
            print(tabulate.tabulate(books_ratings.get_avg_by_title_author(conn, author, book)))
        elif opt == '5':
            conn = connect_books.connect()
            print(f"\nThe average rating for the user with the most reviews is: ", round((books_ratings.avg_rating_most_reviews_user(conn)), 2), "\n")
        elif opt == '6':
            new_id = input("Enter a new user id: ")
            location = input("Enter a location: ")
            age = input("Enter an age: ")
            conn = connect_books.connect()
            print(books_ratings.add_user(conn, new_id, location, age))
        elif opt == '7':
            title = input("Enter a title: ")
            author = input("Enter an author: ")
            year = input("Enter a year: ")
            publisher = input("Enter a publisher: ")
            small = input("Enter a small image: ")
            medium = input("Enter a medium image: ")
            large = input("Enter a large image: ")
            isbn = input("Enter an ISBN: ")
            conn = connect_books.connect()
            books_ratings.insert_book(conn, title, author, int(year), publisher, small, medium, large, isbn)
        elif opt == '8':
            id = input("Enter a user id: ")
            isbn = input("Enter an ISBN: ")
            book_rating = input("Enter a rating: ")
            while not book_rating.isnumeric() and 10 < int(book_rating) < 0:
                book_rating = input("Enter a valid number:")
            conn = connect_books.connect()
            books_ratings.add_review(conn, id, isbn, book_rating)
        elif opt == '9':
            conn = connect_books.connect()
            n = input("Enter the number of authors: ")
            while not n.isnumeric():
                n = input("Enter a valid number:")
            if n.isnumeric():
                books_printed = 10
                print(tabulate.tabulate(books_ratings.top_n_authors(conn, n, 0)))
                while books_printed < int(n):
                    enter = input("Press Enter to continue")
                    print(tabulate.tabulate(br.top_n_authors(conn, n, books_printed)))
                    books_printed += 10
        elif opt == '10':
            conn = connect_books.connect()
            number_books = input("# of top books:")
            while not number_books.isnumeric():
                number_books = input("Enter a valid number:")
            if number_books.isnumeric():
                books_printed = 10
                print(tabulate.tabulate(br.top_n_books(conn, number_books, 0)))
                while books_printed < int(number_books):
                    enter = input("Press Enter to continue")
                    print(tabulate.tabulate(br.top_n_books(conn, int(number_books), books_printed)))
                    books_printed += 10