import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

base_dir = "/Users/jaxlub/Documents/GitHub"
priv_key = "jalubk20-cs345fall22-firebase-adminsdk-xus9l-f9dc5a887b.json"

cred = credentials.Certificate(f'{base_dir}/{priv_key}')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Do all 4 crud operations on the students operation
