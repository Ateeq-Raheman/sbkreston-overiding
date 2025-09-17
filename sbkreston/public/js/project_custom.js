frappe.provide("sbkreston");

frappe.ui.form.on("Project", {
    refresh: function (frm) {
        if (frappe.user_roles.includes("Projects Manager")) {
            if (frm.is_new()) {
                // Disable save only for new (unsaved) projects
                frm.disable_save();
                frm.page.clear_primary_action();

                // Show Force Create Project button
                frm.page.set_primary_action("Save", function () {
                    sbkreston.force_create_project(frm);
                });
            } else {
                // Enable save for existing projects
                frm.enable_save();
                frm.page.clear_primary_action();
                frm.page.set_primary_action(__("Save"), () => frm.save());
            }
        }
    }
});

sbkreston.force_create_project = function (frm) {
    frappe.dom.freeze("Creating Project... Please wait");

    frappe.call({
        method: "sbkreston.sbkreston_app.project.force_create_project",
        args: {
            project_name: frm.doc.project_name,
            department: frm.doc.department,
            project_type: frm.doc.project_type,
            expected_start_date: frm.doc.expected_start_date,
            expected_end_date: frm.doc.expected_end_date,
            branch: frm.doc.branch,
            company: frm.doc.company
        },
        callback: function (r) {
            frappe.dom.unfreeze();
            if (!r.exc) {
                frappe.msgprint("Project created: " + r.message);
                frappe.set_route("Form", "Project", r.message);
            }
        }
    });
};
