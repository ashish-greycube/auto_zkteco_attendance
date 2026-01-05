import frappe
from frappe.utils.response import build_response
from werkzeug.wrappers import Response
from frappe.utils import cstr, get_site_name

import os


def log_request():
    '''Logs all requests to site-name/logs/auto_zkteco.log'''
    frappe.logger("auto_zkteco", allow_site=frappe.local.site).error(
        {
            "raw_body": (
                frappe.request.get_data(as_text=True)
                if hasattr(frappe.request, "get_data")
                else None
            ),
            "query_params": frappe.form_dict or {}
        }
    )


def parse_attlog(raw: str):
    records = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        cols = line.split("\t")

        # Defensive: some devices may send extra trailing tabs
        while len(cols) < 7:
            cols.append("")

        records.append({
            "pin": cols[0],
            "datetime": cols[1],
            "verify_mode": int(cols[2]) if cols[2] else None,
            "status": int(cols[3]) if cols[3] else None,
            "work_code": cols[4] or None,
            "reserved1": int(cols[5]) if cols[5] else None,
            "reserved2": int(cols[6]) if cols[6] else None,
        })

    return records


class CustomAPIRenderer:
    def __init__(self, path, status_code=None):
        self.path = path
        self.status_code = status_code or 200

    def can_render(self):
        return self.path.startswith("iclock")

    def render(self):
        log_request()

        result = {}

        try:

            query_params = frappe.form_dict or {}

            if query_params.get("table") == "ATTLOG":
                # Process Attendance log

                raw_text = frappe.request.get_data(as_text=True) or ""

                result = dict(body_data=parse_attlog(
                    raw_text), query_params=query_params)

                frappe.log_error(title="ZkTeco ATTLOG request", message=result)
            else:
                # add other processing here
                pass

        except Exception as e:
            frappe.log_error(e)

        return Response("OK", mimetype="text/plain")

        # frappe.local.response = result
        # return build_response("json")
