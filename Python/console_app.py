import connect_books as cb
import books_ratings as br
import psycopg2 as pg
import tabulate


def menu() -> str:
    """
    Present an option to the user and return a valid option
    :return: 1, 2, Q, q
    """
    while True:
        print("1) get book by ISBN")
        print("2) Look up book by author")
        print("Q) Quit")
        opt = input("> ")
        if opt in ['1', '2', 'Q', 'q']:
            return opt


if __name__ == "__main__":
    conn = cb.connect()
    while True:
        opt = menu()
        if opt == '1':
            # get title by ISBN
            isbn = input("ISBN: ")
            title = br.get_title_by_isbn(conn, isbn)
            if title == None:
                print("No Book with that ISBN")
            else:
                print(title)

        elif opt == '2':
            # get books by author
            author = input("Author: ")
            books = br.get_books_by_author(conn, author)

            if books is None:
                print("No Books by that Author")
            else:
                print(tabulate.tabulate(books, tablefmt="fancy_grid",
                                        headers=["Book", "Year", "Publisher", "ISBN"]))
        elif opt in ['q', 'Q']:
            break
