from customer_googlecloud import CustomerGoogleCloud

if __name__ == '__main__':
    cust = CustomerGoogleCloud()
    cust.create_table()
    cust.insert(8, 'Bobbo', 'Baggins', '1234-1234-1234-1234', '04/25', '123')
    #cust.insert(6, 'Bilbo', 'Baggins', '1234-1234-1234-1234', '04/25', '123')
    print(cust.lookup(8))
    cust.delete(1)
    #cust.insert(1, 'Bilbo', 'Baggins', '1234-1234-1234-1234', '04/25', '123')
