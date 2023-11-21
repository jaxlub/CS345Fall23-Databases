import customer

if __name__ == '__main__':
    cust = customer.Customer()
    cust.create_table()
    cust.insert(1, 'Bilbo', 'Baggins', '1234-1234-1234-1234', '04/25', '123')
