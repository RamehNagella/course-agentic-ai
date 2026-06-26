Below is a complete MCP (Model Context Protocol) server for a Leave Management System using FastMCP. It includes:

✅ Apply Leave
✅ Approve Leave
✅ Reject Leave
✅ View Leave Balance
✅ View Leave History
✅ List Pending Requests
✅ Employee Information Resource
✅ Leave Policy Resource
✅ Prompt to generate leave application

from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Create MCP Server

mcp = FastMCP("Leave Management System", json_response=True)

# -------------------------------------------------------------------

# Dummy Database

# -------------------------------------------------------------------

employees = {
101: {
"name": "Ramesh",
"department": "Engineering",
"leave_balance": 15,
"history": []
},
102: {
"name": "John",
"department": "HR",
"leave_balance": 10,
"history": []
}
}

leave_requests = []

# -------------------------------------------------------------------

# TOOLS

# -------------------------------------------------------------------

@mcp.tool()
def apply_leave(
employee_id: int,
start_date: str,
end_date: str,
reason: str,
days: int
):
"""
Apply for leave.
"""

    if employee_id not in employees:
        return {"status": "error", "message": "Employee not found"}

    employee = employees[employee_id]

    if employee["leave_balance"] < days:
        return {
            "status": "failed",
            "message": "Insufficient leave balance"
        }

    request_id = len(leave_requests) + 1

    request = {
        "request_id": request_id,
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "start_date": start_date,
        "end_date": end_date,
        "days": days,
        "reason": reason,
        "status": "Pending",
        "applied_on": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    leave_requests.append(request)

    employee["history"].append(request)

    return {
        "status": "success",
        "message": "Leave request submitted",
        "request": request
    }

@mcp.tool()
def approve_leave(request_id: int):
"""
Approve leave request.
"""

    for request in leave_requests:

        if request["request_id"] == request_id:

            if request["status"] != "Pending":
                return {
                    "status": "failed",
                    "message": "Request already processed"
                }

            employee = employees[request["employee_id"]]

            if employee["leave_balance"] < request["days"]:
                return {
                    "status": "failed",
                    "message": "Not enough leave balance"
                }

            employee["leave_balance"] -= request["days"]
            request["status"] = "Approved"

            return {
                "status": "success",
                "message": "Leave approved",
                "remaining_balance": employee["leave_balance"]
            }

    return {"status": "error", "message": "Request not found"}

@mcp.tool()
def reject_leave(request_id: int, reason: str):
"""
Reject leave request.
"""

    for request in leave_requests:

        if request["request_id"] == request_id:

            request["status"] = "Rejected"
            request["rejection_reason"] = reason

            return {
                "status": "success",
                "message": "Leave rejected"
            }

    return {"status": "error", "message": "Request not found"}

@mcp.tool()
def get_leave_balance(employee_id: int):
"""
Get employee leave balance.
"""

    if employee_id not in employees:
        return {"status": "error", "message": "Employee not found"}

    employee = employees[employee_id]

    return {
        "employee": employee["name"],
        "leave_balance": employee["leave_balance"]
    }

@mcp.tool()
def leave_history(employee_id: int):
"""
View leave history.
"""

    if employee_id not in employees:
        return {"status": "error"}

    return employees[employee_id]["history"]

@mcp.tool()
def pending_requests():
"""
List all pending leave requests.
"""

    return [
        request
        for request in leave_requests
        if request["status"] == "Pending"
    ]

# -------------------------------------------------------------------

# RESOURCES

# -------------------------------------------------------------------

@mcp.resource("employee://{employee_id}")
def employee_details(employee_id: str):
"""
Employee details resource.
"""

    emp = employees.get(int(employee_id))

    if not emp:
        return "Employee not found"

    return emp

@mcp.resource("leave-policy://company")
def leave_policy():
"""
Company leave policy.
"""

    return """

Company Leave Policy

1. Annual Leave : 20 days
2. Sick Leave : 10 days
3. Casual Leave : 8 days
4. Maternity Leave : 180 days
5. Paternity Leave : 15 days

Rules:

- Manager approval required.
- Apply at least 2 days before leave.
- Emergency leave allowed for medical reasons.
  """

# -------------------------------------------------------------------

# PROMPTS

# -------------------------------------------------------------------

@mcp.prompt()
def write_leave_application(
employee_name: str,
days: int,
reason: str
):
"""
Generate a leave application.
"""

    return f"""

Write a professional leave application.

Employee Name: {employee_name}
Leave Duration: {days} day(s)
Reason: {reason}

Keep it polite and professional.
"""

# -------------------------------------------------------------------

# RUN SERVER

# -------------------------------------------------------------------

if **name** == "**main**":
mcp.run(transport="streamable-http")

Example MCP interactions
Apply Leave
Tool: apply_leave

Input:
employee_id = 101
start_date = "2026-06-30"
end_date = "2026-07-02"
days = 3
reason = "Family Function"

Response

{
"status": "success",
"message": "Leave request submitted",
"request": {
"request_id": 1,
"status": "Pending"
}
}
Approve Leave
Tool:
approve_leave(1)
Check Leave Balance
Tool:
get_leave_balance(101)
Get Employee Resource
employee://101
Company Policy Resource
leave-policy://company
Prompt Example
write_leave_application(
employee_name="Ramesh",
days=2,
reason="Medical Appointment"
)

This structure demonstrates the three core MCP concepts:

# 1. Tools for actions that change or retrieve data (apply, approve, reject, balance, history).

# 2. Resources for read-only information (employee details, leave policy).

# 3. Prompts for reusable AI-generated content (professional leave application). It is a good foundation for integrating with a real database and an HRMS backend later.

The above code is going to use claude desktop as tool for applying leaves is that ok right, the above code works fine right?

Yes, conceptually it's correct, and it can be used from a Claude Desktop MCP client. However, there are a few things to be aware of before expecting it to work in a real-world scenario.

What will work

If you configure your MCP server in Claude Desktop, Claude can call tools like:

apply_leave()
approve_leave()
reject_leave()
get_leave_balance()
leave_history()

For example, if you ask Claude:

"Apply leave for employee 101 from July 10 to July 12 for a family function."

Claude will determine that it should call:

apply_leave(
employee_id=101,
start_date="2026-07-10",
end_date="2026-07-12",
reason="Family Function",
days=3
)

Your server returns the JSON response, and Claude explains the result in natural language.

However, there are some limitations

1. Data is stored only in memory

Right now you have:

employees = {
...
}

leave_requests = []

Whenever you stop the server,

python server.py

all leave requests disappear.

For production, you'd use:

SQLite
PostgreSQL
MySQL
MongoDB

instead of Python dictionaries.

2. No authentication

Right now anyone can do:

approve_leave(1)

even if they're not a manager.

Normally you'd have:

Employee
Manager
HR
Admin

with role-based permissions.

3. Dates are not validated

Someone could call

apply_leave(
employee_id=101,
start_date="2026-08-10",
end_date="2026-08-01",
days=5,
reason="Vacation"
)

and your code would still accept it.

You should validate:

start_date ≤ end_date
days > 0
dates aren't in the past (if required)
days matches the date range (or calculate it automatically) 4. Duplicate approvals

You already prevent approving the same request twice:

if request["status"] != "Pending":

That's good.

5. Resources

These work nicely.

For example:

employee://101

returns employee information.

And

leave-policy://company

returns the leave policy.

Claude can use these when answering questions like:

"What is my leave balance?"

or

"What is the company's maternity leave policy?"

6. Prompt

This is also correct.

Claude can use

write_leave_application(...)

to generate a professional leave application.

One improvement I'd make

Instead of asking the caller to provide days, calculate it automatically from the dates.

Current:

apply_leave(
employee_id,
start_date,
end_date,
reason,
days
)

Better:

apply_leave(
employee_id,
start_date,
end_date,
reason
)

Then compute:

from datetime import datetime

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

days = (end - start).days + 1

This avoids users accidentally specifying:

July 1
July 5
days = 2

which would be inconsistent.

Overall assessment

For learning MCP and integrating with Claude Desktop, this server is a good starting point.

I'd rate it:

MCP structure (Tools, Resources, Prompts): ⭐⭐⭐⭐⭐ (5/5)
Claude Desktop compatibility: ⭐⭐⭐⭐⭐ (5/5), assuming the server is configured correctly.
Production readiness: ⭐⭐☆☆☆ (2/5), because it lacks persistent storage, authentication, input validation, logging, and role-based access control.

If your goal is to learn MCP for interviews or build a demo, this is absolutely fine. If you want to build a real HR leave management MCP server, the next step would be replacing the in-memory data structures with a database and adding authentication and validation.
