import frappe

@frappe.whitelist()
def force_create_project(project_name, branch=None, company=None, department=None):
    if "Projects Manager" not in frappe.get_roles(frappe.session.user):
        frappe.throw("Not allowed")
    
    # Create the project
    doc = frappe.get_doc({
        "doctype": "Project",
        "project_name": project_name,
        "status": "Open",
        "is_active": "Yes",
        "branch": branch,
        "company": company,
        "department": department
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    restricted_roles = {"System Manager", "Projects User", "Super Admin"}
    user = frappe.session.user
    user_roles = set(frappe.get_roles(user))

    if not (user_roles & restricted_roles):
        user_doc = frappe.get_doc("User", user)
        user_doc.append("user_projects", {
            "project": doc.name,
            "branch": branch,
            "company": company,
            "department": department
        })
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()

    return doc.name
