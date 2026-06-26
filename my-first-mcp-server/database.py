# steps to get employees data from database 
# using mongodb 
#  install mongodb driver:
# uv add pymongo or pip install pymongo

# from pymongo import MongoClient

# # MongoDB connection
# client = MongoClient("mongodb://localhost:27017")

# db= client["leave_management"]

# # employees_collection = db.collection("employees") or 
# employees_collection = db["employees"]

# # # sample document 
# # {
# #     "_id": ObjectId("686..."),
# #     "employee_id": 101,
# #     "name": "Ramesh",
# #     "department": "Engineering",
# #     "leave_balance": 15,
# #     "history": []
# # }