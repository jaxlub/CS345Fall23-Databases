from customer_firestore import CustomerFireStore

cust = CustomerFireStore()
cust.insert(1, 'Bilbo', 'Baggins', '1234-1234-1234-1234', '04/25', '123')
cust.insert(2, 'Bobbo', 'Baggins', '1234-1234-1234-1234', '04/25', '123')
cust.lookup(1)
cust.delete(2)

