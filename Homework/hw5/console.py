import books_ratings
import connect_books
import tabulate
import Ratings
import Users
import Books
import connect_books as cb
import books_ratings as br
import psycopg as pg

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
    ratings = Ratings.Ratings(conn)
    users = Users.Users(conn)
    books = Books.Books(conn)
    while True:
        opt = menu()
        if opt == '1':
            isbn = input("Enter an ISBN: ")
            print(f"\n", books.get_title_by_isbn(isbn), "\n")
            # get title by ISBN
        elif opt == '2':
            author = input("Enter an author: ")
            a = books.get_books_by_author(author)
            if a is None:
                print("Error: No author found with that name")
            else:
                print(tabulate.tabulate(books.get_books_by_author(author),
                                        headers = ["Title", "Year", "Publisher", "ISBN"],
                                        tablefmt= "fancy_outline"))

            # get books by author
        elif opt in ['Q','q']:
            break
        elif opt == '3':
            author = input("Enter an author: ")
            if books.valid_author(author):
                print(tabulate.tabulate(ratings.avg_rating_by_author(author)))
            else:
                print("Error: No author")
        elif opt == '4':
            author = input("Enter the author: ")
            book = input("Enter a book: ")
            if books.valid_books(book) and books.valid_author(author):
                print(tabulate.tabulate(ratings.avg_rating_by_author(author)))
            else:
                print("Error: No such title or author")
        elif opt == '5':
            print(f"\nThe average rating for the user with the most reviews is: ",
                  round((users.avg_rating_most_reviews_user()), 2), "\n")
        elif opt == '6':
            new_id = input("Enter a new user id: ")
            location = input("Enter a location: ")
            age = input("Enter an age: ")
            users.add_user(new_id, location, age)
        elif opt == '7':
            title = input("Enter a title: ")
            author = input("Enter an author: ")
            year = input("Enter a year: ")
            publisher = input("Enter a publisher: ")
            small = input("Enter a small image: ")
            medium = input("Enter a medium image: ")
            large = input("Enter a large image: ")
            isbn = input("Enter an ISBN: ")
            books.insert_book(title, author, int(year), publisher, small, medium, large, isbn)
        elif opt == '8':
            id = input("Enter a user id: ")
            isbn = input("Enter an ISBN: ")
            book_rating = input("Enter a rating: ")
            while not book_rating.isnumeric():
                book_rating = input("Enter a valid number:")
            while not 0 < int(book_rating) < 10:
                book_rating = input("Enter a valid number:")
            ratings.add_review(id, isbn, book_rating)
        elif opt == '9':
            n = input("Enter the number of authors: ")
            while not n.isnumeric():
                n = input("Enter a valid number:")
            if n.isnumeric():
                books_printed = 10
                print(tabulate.tabulate(books.top_n_authors(n, str("0"))))
                while books_printed < int(n):
                    enter = input("Press Enter to continue")
                    print(tabulate.tabulate(books.top_n_authors(n, str(books_printed))))
                    books_printed += 10
                input("Press Enter to continue")
        elif opt == '10':
            number_books = input("# of top books:")
            while not number_books.isnumeric():
                number_books = input("Enter a valid number:")
            if number_books.isnumeric():
                books_printed = 10
                print(tabulate.tabulate(books.top_n_books(number_books, str("0"))))
                while books_printed < int(number_books):
                    # enter = input("Press Enter to continue")
                    print(tabulate.tabulate(books.top_n_books(number_books, str(books_printed))))
                    books_printed += 10
                    input("Press Enter to continue")