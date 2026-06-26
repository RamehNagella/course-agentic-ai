# mcp server main have 3 components
# Tools  Resources   Prompts

# Tools are nothing but our required functionalities from the mcp
# here in our application: Leave Management System 
# we need to have 
# 1. employees data 
# 2. applying leave functionality 
# 3. check leaves functionality 
# 4. reject leave functionality 
# 5. balcance leaves functionality 
# 6. leaves history functionality 
# 7. approve leave functionality

from mcp.server.fastmcp import FastMCP
from typing import List
# from database import employees_collection

# employees data 
# In memory mock database with 20 leave days to start

employee_data = {
  "E001":{"name":"Ramesh", "department":"Devlopment", "leave_balance": 18, "history":["2024-12-25", "2025-01-01"]},
  "E002":{"name":"Ravi", "department":"Testing","leave_balance": 15, "history":["2024-10-25", "2025-01-14"]}
}


print(employee_data)
# Create mcp server 
mcp = FastMCP("LeaveManager")



# Tool: Check leave balance 
@mcp.tool()
def get_leave_balance(employee_id: str):
#   check employee id is present in db or not 
#   1.take employee id  and get emplyee data from db 
#   2. get the balance leaves availble 
#   3. if balance leaves are greater then 0 return no of balance leaves are there 

  """
  Get employee leave balance.
  """  
  if employee_id not in employee_data:
    return {"status": "error", "message":"Employee not found."}
  
  employee = employee_data.get(employee_id)
#   print(employee)
  return {
    "employee": employee["name"],
    "leave_balance": employee["leave_balance"],
    "leaves_history":employee["history"]
  }

# Tool: Apply for leave with specific dates
@mcp.tool()
def apply_leave(employee_id: str, leave_dates:List[str])->str:
  
  """
  Apply leave for an employee on specific dates (e.g., ["2025-04-17", "2025-05-01"])
  """
  employee = get_leave_balance(employee_id)

  available_leaves = employee["leave_balance"]

  if not employee:
    return f"employee not found in database"
    
  requested_days = len(leave_dates)
  
  if employee["leave_balance"] < requested_days:
    return f" Insufficient leave balance. You requested {requested_days} day(s) but have only {available_leaves}"
  

  employee_data.get(employee_id)["leave_balance"] -= requested_days
#   employee_data.get(employee_id)["history"].append(leave_dates) append() makes adds list inside list 
  employee_data.get(employee_id)["history"].extend(leave_dates) 

  return f"Leave applied for {requested_days} day(s).Remaining balance: {employee_data.get(employee_id)["leave_balance"]}" 

# Resource:  leaves history
@mcp.tool()
def get_leaves_history(employee_id: str)->str:
    """
    Get leave history for the employee
    """
    employee = get_leave_balance(employee_id)
    # print("RRR> ",employee)
    if employee:
      leaves_history = ", ".join(employee["leaves_history"]) if employee["leaves_history"] else "No leaves taken."
      return f"Leave history for {employee_id}: {leaves_history}"
    return "Emplyee ID not found."

#approve leaves 
@mcp.tool()
def approve_leave(employee_id: str)->str:
  pass 

if __name__ == "__main__":

#   print(get_leave_balance("E001"))
#   print(get_leaves_history("E001"))
    mcp.run()

#  -------------------------------------------------

# # if data is retrieving from DB the employee data is 
# @mcp.tool()
# def get_emplyee(employee_id:str):
#     employee = employees_collection.find_one(
#     {"employee_id": employee_id},
#     {"_id":0}
#     )
    
#     if employee is None:
#        return {
#           "status":"error",
#           "message": "Employee not found"
#        }
#     return employee

# @mcp.tool()
# def get_leave_balance(employee_id: str):
#   employee = get_employee(employee_id)

#   if employee is None:
#     return {
#       "status":"error",
#       "message":"Employee not found"
#     }
  
#   return {
#     "employee": employee["name"],
#     "leave_balance":employee["leave_balance"],
#     "leaves_history":employee["history"]
#   }


# Tool: Apply for leave with specific dates
# @mcp.tool()
# def apply_leave(employee_id: str, leave_dates:List[str])->str:
  
#   """
#   Apply leave for an employee on specific dates (e.g., ["2025-04-17", "2025-05-01"])
#   """
#   employee = get_leave_balance(employee_id)

#   available_leaves = employee["leave_balance"]

#   if not employee:
#     return f"employee not found in database"
    
#   requested_days = len(leave_dates)
  
#   if employee["leave_balance"] < requested_days:
#     return f" Insufficient leave balance. You requested {requested_days} day(s) but have only {available_leaves}"
  

# #   employee_data.get(employee_id)["leave_balance"] -= requested_days
#   employees_collection.update_one({"employee_id": employee_id},{
#       "$push":{
#         "history": {
#           "$each": leave_dates
#         }
#       }
#     })
#   employees_collection.update_one({"employee_id":employee_id},{
#     "$inc":{
#       "leave_balance": -requested_days
#     }
#   })
# # #   employee_data.get(employee_id)["history"].append(leave_dates) append() makes adds list inside list 
# #   employee_data.get(employee_id)["history"].extend(leave_dates) 

#   return f"Leave applied for {requested_days} day(s).Remaining balance: {employee_data.get(employee_id)["leave_balance"]}" 


#  -------------------------------------------------
  