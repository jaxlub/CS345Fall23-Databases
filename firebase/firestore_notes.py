import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

base_dir = "/Users/jaxlub/Documents/GitHub"
priv_key = "jalubk20-cs345fall22-firebase-adminsdk-xus9l-f9dc5a887b.json"

cred = credentials.Certificate(f'{base_dir}/{priv_key}')
firebase_admin.initialize_app(cred)

# reference to firestore DB
db = firestore.client()

# Create a laptops collections
coll = db.collection("students")

# add a document
doc_ref = coll.document('student3')
doc_ref.set(
    {
        "name": {"first": "Draco", "last": "Malfoy"},
        "course": {
            "c1": {"Year": 2023, "course_name": "Intro to dark arts", "course_num": "DA101", "semester": "Spring"}},
    }
)

# Read - if ID is known
doc_ref = coll.document('student1')
obj = doc_ref.get().to_dict()
print(obj)

# Update
doc_ref = coll.document('student1')
doc_ref.set(
    {'courses': {'c1': {'semester': 'Fall', 'Year': 2022, 'course_name': 'Intro Potions', 'course_num': 'P101'},
                 'c2': {'semester': 'Fall', 'Year': '2023', 'course_name': 'Intro to Dark Arts',
                        'course_num': 'DA101'}}, 'name': {'last': 'Potter', 'first': 'Harry'}}
)
# Delete
doc_ref = coll.document("student3")
doc_ref.delete()
coll2 = db.collection("Laptops")

# look-up
docs = coll2.where("brand", "==","Apple").stream()
for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')