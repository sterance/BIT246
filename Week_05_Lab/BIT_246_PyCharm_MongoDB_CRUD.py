"""
 PYTHON + MONGODB CRUD
============================

This program is designed for beginners using PyCharm.

WHAT WILL WE LEARN?
-------------------
CRUD means:
C = Create -> add new information
R = Read   -> look at information
U = Update -> change information
D = Delete -> remove information

MongoDB stores information as DOCUMENTS.

Example:
{
    "name": "Emma",
    "subject": "Python",
    "mark": 85
}

MongoDB organises data like this:

Database
   ↓
Collection
   ↓
Document

BEFORE YOU RUN THIS PROGRAM IN PYCHARM
--------------------------------------
1. Open PyCharm.
2. Create or open a Python project.
3. Open the PyCharm Terminal.
4. Type:

       pip install pymongo dnspython pandas

5. Press Enter.
6. Log in to MongoDB Atlas.
7. Make sure you have:
   - a database user
   - a password
   - your current computer/network IP allowed in Atlas Network Access
8. In Atlas choose:
   Database -> Connect -> Drivers -> Python
9. Copy the connection string.
10. Run this Python program.
11. Paste your connection string when PyCharm asks for it.

IMPORTANT SAFETY RULE:
Never put your real MongoDB password directly inside code that you share.
This program uses getpass(), so your connection string is not shown on screen.
"""

# ------------------------------------------------------------
# STEP 1: IMPORT THE TOOLS
# ------------------------------------------------------------

from getpass import getpass
from pprint import pprint

import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi

print("\nSTEP 1")
print("MongoDB tools are ready.")


# ------------------------------------------------------------
# STEP 2: GET THE MONGODB ATLAS CONNECTION STRING
# ------------------------------------------------------------

print("""
STEP 2
Paste your MongoDB Atlas connection string below.

Example shape:
mongodb+srv://USERNAME:PASSWORD@cluster-name.mongodb.net/

Your real connection string will be different.
""")

MONGO_URI = getpass("MongoDB Atlas connection string: ")


# ------------------------------------------------------------
# STEP 3: CREATE THE CONNECTION
# ------------------------------------------------------------

# MongoClient is like a doorway from Python to MongoDB Atlas.
client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1"),
    serverSelectionTimeoutMS=10000
)

print("\nSTEP 3")
print("MongoClient was created.")


# ------------------------------------------------------------
# STEP 4: TEST THE CONNECTION
# ------------------------------------------------------------

try:
    client.admin.command("ping")
    print("SUCCESS: PyCharm is connected to MongoDB Atlas.")
except Exception as error:
    print("\nThe connection did not work.")
    print("Please check:")
    print("1. Your Atlas username and password.")
    print("2. Your Atlas Network Access / IP Access List.")
    print("3. Your internet connection.")
    print("\nTechnical message:")
    print(error)
    client.close()
    raise SystemExit


# ------------------------------------------------------------
# STEP 5: CHOOSE A DATABASE AND COLLECTION
# ------------------------------------------------------------

db = client["school_database"]
students = db["students"]

print("\nSTEP 5")
print("Database:", db.name)
print("Collection:", students.name)

# For this classroom demonstration, remove only the sample names
# used by this lesson. This makes repeated runs easier to understand.
lesson_names = [
    "Emma", "Noah", "Mia", "Oliver", "Ava",
    "Liam", "Sophie", "Jack"
]

students.delete_many({"name": {"$in": lesson_names}})

print("Old lesson examples were cleared so we can start fresh.")


# ------------------------------------------------------------
# HELPER FUNCTION: SHOW DOCUMENTS AS A TABLE
# ------------------------------------------------------------

def show_documents(query=None, title="Results", projection=None):
    """
    Find MongoDB documents and print them as a simple table.

    query      = what we are searching for
    title      = heading displayed above the answer
    projection = which fields we want to show
    """
    if query is None:
        query = {}

    records = list(students.find(query, projection))

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if not records:
        print("There are no documents to show.")
        return pd.DataFrame()

    # MongoDB's _id is useful, but it can make a beginner table wide.
    # Change ObjectId values to text so pandas can print them neatly.
    for record in records:
        if "_id" in record:
            record["_id"] = str(record["_id"])

    table = pd.DataFrame(records)
    print(table.to_string(index=False))
    return table


# ------------------------------------------------------------
# STEP 6: CREATE A PYTHON DICTIONARY
# ------------------------------------------------------------

student = {
    "name": "Emma",
    "subject": "Python",
    "mark": 85,
    "year_level": 5
}

print("\nSTEP 6")
print("This Python dictionary will become a MongoDB document:")
pprint(student)


# ------------------------------------------------------------
# CRUD 1: CREATE
# CREATE MEANS "ADD NEW DATA"
# ------------------------------------------------------------

print("\nCRUD 1 - CREATE")
print("CREATE means add new information.")

result = students.insert_one(student)

print("Emma was added.")
print("MongoDB gave Emma this unique _id:")
print(result.inserted_id)


# Add several students.
more_students = [
    {"name": "Noah", "subject": "Database", "mark": 78, "year_level": 5},
    {"name": "Mia", "subject": "Python", "mark": 92, "year_level": 5},
    {"name": "Oliver", "subject": "Cyber Security", "mark": 74, "year_level": 5},
    {"name": "Ava", "subject": "Database", "mark": 88, "year_level": 5}
]

result = students.insert_many(more_students)

print("More students were added.")
print("Number added:", len(result.inserted_ids))

show_documents(title="Students after CREATE")


# ------------------------------------------------------------
# CRUD 2: READ
# READ MEANS "LOOK AT DATA"
# ------------------------------------------------------------

print("\nCRUD 2 - READ")
print("READ means look at stored information.")

# Find Emma.
emma = students.find_one({"name": "Emma"})

print("\nREAD 1 - Find Emma")
pprint(emma)

# Find all students.
show_documents(
    title="READ 2 - All students"
)

# Marks of 80 or higher.
# $gte means greater than or equal to.
show_documents(
    {"mark": {"$gte": 80}},
    title="READ 3 - Marks of 80 or higher"
)

# Find only Python students.
show_documents(
    {"subject": "Python"},
    title="READ 4 - Python students"
)

# Projection means choosing which fields to show.
show_documents(
    {},
    title="READ 5 - Selected fields only",
    projection={"_id": 0, "name": 1, "subject": 1, "mark": 1}
)


# ------------------------------------------------------------
# CRUD 3: UPDATE
# UPDATE MEANS "CHANGE DATA"
# ------------------------------------------------------------

print("\nCRUD 3 - UPDATE")
print("UPDATE means change information.")

result = students.update_one(
    {"name": "Noah"},
    {"$set": {"mark": 82}}
)

print("Noah matched:", result.matched_count)
print("Noah changed:", result.modified_count)

print("\nCheck Noah:")
pprint(students.find_one({"name": "Noah"}))


# Change Oliver's subject and mark.
students.update_one(
    {"name": "Oliver"},
    {"$set": {"subject": "Python", "mark": 80}}
)

print("\nOliver after UPDATE:")
pprint(students.find_one({"name": "Oliver"}))


# $inc means increase a number.
students.update_one(
    {"name": "Mia"},
    {"$inc": {"mark": 2}}
)

print("\nMia received 2 bonus marks:")
pprint(students.find_one({"name": "Mia"}))


# ------------------------------------------------------------
# CRUD 4: DELETE
# DELETE MEANS "REMOVE DATA"
# ------------------------------------------------------------

print("\nCRUD 4 - DELETE")
print("DELETE means remove information.")

result = students.delete_one({"name": "Ava"})

print("Number of documents deleted:", result.deleted_count)

show_documents(
    title="Students after DELETE"
)


# ------------------------------------------------------------
# STEP 7: COUNT STUDENTS
# ------------------------------------------------------------

total = students.count_documents({})
python_count = students.count_documents({"subject": "Python"})

print("\nSTEP 7")
print("Total students:", total)
print("Python students:", python_count)


# ------------------------------------------------------------
# STEP 8: SORT STUDENTS BY MARK
# ------------------------------------------------------------

sorted_students = list(
    students.find({}, {"_id": 0}).sort("mark", -1)
)

print("\nSTEP 8 - Highest mark first")
print(pd.DataFrame(sorted_students).to_string(index=False))


# ------------------------------------------------------------
# STEP 9: CALCULATE AN AVERAGE WITH PANDAS
# ------------------------------------------------------------

df = pd.DataFrame(
    list(students.find({}, {"_id": 0}))
)

if not df.empty:
    print("\nSTEP 9")
    print("Average mark:", round(df["mark"].mean(), 2))


# ------------------------------------------------------------
# STEP 10: MONGODB AGGREGATION
# ------------------------------------------------------------

# $group puts matching values into groups.
# $avg calculates an average.
pipeline = [
    {
        "$group": {
            "_id": "$subject",
            "average_mark": {"$avg": "$mark"}
        }
    },
    {
        "$sort": {"average_mark": -1}
    }
]

average_by_subject = list(students.aggregate(pipeline))

print("\nSTEP 10 - Average mark by subject")
print(pd.DataFrame(average_by_subject).to_string(index=False))


# ------------------------------------------------------------
# STEP 11: MONGODB CAN STORE A LIST
# ------------------------------------------------------------

liam = {
    "name": "Liam",
    "subject": "Python",
    "mark": 90,
    "year_level": 5,
    "hobbies": ["football", "drawing", "coding"]
}

students.insert_one(liam)

print("\nSTEP 11 - Liam has a list of hobbies")
pprint(students.find_one({"name": "Liam"}))


# ------------------------------------------------------------
# STEP 12: MONGODB CAN STORE A NESTED DOCUMENT
# ------------------------------------------------------------

sophie = {
    "name": "Sophie",
    "subject": "Database",
    "mark": 86,
    "year_level": 5,
    "contact": {
        "city": "Melbourne",
        "country": "Australia"
    }
}

students.insert_one(sophie)

print("\nSTEP 12 - Sophie has information inside contact")
pprint(students.find_one({"name": "Sophie"}))


# MongoDB uses dot notation to search inside nested information.
show_documents(
    {"contact.country": "Australia"},
    title="Students whose contact.country is Australia",
    projection={"_id": 0}
)


# ------------------------------------------------------------
# STEP 13: EXPORT DATA TO CSV
# ------------------------------------------------------------

export_df = pd.DataFrame(
    list(students.find({}, {"_id": 0}))
)

export_df.to_csv(
    "mongodb_students.csv",
    index=False
)

print("\nSTEP 13")
print("mongodb_students.csv was created.")
print("Look for it inside your PyCharm project folder.")


# ------------------------------------------------------------
# STUDENT PRACTICE
# ------------------------------------------------------------

print("""
============================================================
STUDENT PRACTICE
============================================================

Task 1 - CREATE
Add Jack:
subject = Python
mark = 84
year_level = 5

Task 2 - READ
Find Jack.

Task 3 - UPDATE
Change Jack's mark to 89.

Task 4 - DELETE
Delete Jack.

Task 5 - READ
Show all remaining students.

Remember:
CREATE = insert_one() / insert_many()
READ   = find_one() / find()
UPDATE = update_one()
DELETE = delete_one()
""")


# ------------------------------------------------------------
# FINAL STEP: CLOSE THE CONNECTION
# ------------------------------------------------------------

client.close()

print("\nMongoDB connection closed.")
print("Excellent work! You have completed the MongoDB CRUD lesson.")
