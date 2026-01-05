__version__ = "0.0.1"


import frappe
from frappe import _
from werkzeug.wrappers import Response

@frappe.whitelist(allow_guest=True)
def cdata():
    #  frappe.log_error("xyz", frappe.request.data.decode())
    # Frappe uses frappe.request which is similar to Flask's request
    args = frappe.request.args
    sn = args.get("SN")
    table = args.get("table")
    command = args.get("c")

    # Use frappe.logger for production logging (logs to Error Log Doctype)
    # print() works but only shows in the terminal/bench console
    print(f"📡 Device SN={sn}, table={table}, command={command}")
    frappe.log_error("Attendance", f"📡 Device SN={sn}, table={table}, command={command}")

    # Access raw body data
    data = frappe.request.get_data()

    if table == "ATTLOG" and data:
        logs = data.decode("utf-8").strip().splitlines()
        for line in logs:
            print(f"   → Log: {line}")
            frappe.log_error("Attendance", f"   → Log: {line}")
            # Example: Save to Frappe Doc
            # process_attendance_log(line)
        return "OK"
        # return Response("OK", mimetype="text/plain")

    if table == "USER" and data:
        users = data.decode("utf-8").strip().splitlines()
        for line in users:
            print(f"   → User: {line}")
            frappe.log_error("Attendance", f"   → User: {line}")
        
        return "OK"
        # return Response("OK", mimetype="text/plain")

    return "OK"
    # return Response("OK", mimetype="text/plain")


@frappe.whitelist(allow_guest=True)
def getrequest():
    args = frappe.request.args
    sn = args.get("SN")
    
    print(f"📡 Device {sn} is polling for commands")
    frappe.log_error("Attendance", f"📡 Device {sn} is polling for commands")
    # Example command
    command_str = "USER ADD PIN=2001\tName=Test User\tPrivilege=0\tCard=12345678"
    
    return Response(command_str, mimetype="text/plain")

# @app.route("/iclock/cdata", methods=["GET", "POST"])
# def cdata():
#     sn = request.args.get("SN")
#     table = request.args.get("table")
#     command = request.args.get("c")

#     print(f"📡 Device SN={sn}, table={table}, command={command}")

#     if table == "ATTLOG" and request.data:
#         logs = request.data.decode("utf-8").strip().splitlines()
#         for line in logs:
#             print("   → Log:", line)
#         return "OK"

#     if table == "USER" and request.data:
#         users = request.data.decode("utf-8").strip().splitlines()
#         for line in users:
#             print("   → User:", line)
#         return "OK"

#     return "OK"


# @app.route("/iclock/getrequest", methods=["GET"])
# def getrequest():
#     sn = request.args.get("SN")
#     print(f"📡 Device {sn} is polling for commands")

#     # Example: tell device to add a user
#     return "USER ADD PIN=2001\tName=Test User\tPrivilege=0\tCard=12345678"