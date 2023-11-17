import json

empty_object = {}
hobbit = {"First": "Bilbo", "Last": "Baggins"}
print(json.dumps(hobbit))
json.dump(hobbit, open("hobbit.json", "w"), indent=4)  # dump to json file

students = [
    {"name": {"First": "Bob", "Last": "Joe"},
     "courses": [{"course_num": "P101", "Title": "Intro to Potions"},
                 {"course_num": "DA101", "Title": "Intro to Dark Arts"}]},
    {"name": {"First": "Harry", "Last": "Potter"}, "courses": [{"course_num": "P101", "Title": "Intro to Potions"}]}
]

print(json.dumps(students, indent=4))

# Format for storing Bilbos credit card
ccdata = {
    'name': 'Bilbo Baggins',
    'ccnum': '1234-1234-1234-1234',
    'expdate': '04/25',
    'cvv': '123'
}

# Convert ccdat to string
ccdata_str = json.dumps(ccdata)

# convert this to bytes for encryption functions
ccdata_bytes = ccdata_str.encode()

# encrypt and convert to base64
