import frappe

def has_permission(doc=None, ptype="read", user=None):
    if not user:
        user = frappe.session.user

    ptype = ptype.lower()

    # Allow "Projects Manager" to bypass everything
    if "Projects Manager" in frappe.get_roles(user):
        # Ignore user permissions for this request
        frappe.flags.ignore_user_permissions = True
        frappe.flags.ignore_permissions = True  # Extra safety

        if ptype in ["read", "write", "create", "submit", "cancel"]:
            return True

    # Default behavior
    return False



def before_insert(doc, method):
    if "Projects Manager" in frappe.get_roles(frappe.session.user):
        frappe.flags.ignore_permissions = True
