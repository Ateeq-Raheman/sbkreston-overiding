import frappe

def has_permission(doc=None, ptype="read", user=None):
    if not user:
        user = frappe.session.user

    # Allow "Projects Manager" role to do anything
    if "Projects Manager" in frappe.get_roles(user):
        if ptype in ["read", "write", "create", "submit", "cancel"]:
            return True

    # Fallback to default permission checks
    return None
