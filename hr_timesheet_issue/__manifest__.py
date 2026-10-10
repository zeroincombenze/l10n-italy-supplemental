# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "HR - Issue on Timesheets",
    "version": "10.0.1.0.0",
    "category": "HR",
    "summary": "Allow the user to select issue in a timesheet",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/crm",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "depends": [
        "analytic_partner",
        "project_issue_sheet",
        "hr_timesheet_task",
        "hr_timesheet",
    ],
    "data": [
        "views/analytic_line_view.xml",
        "views/hr_timesheet_view.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
    "installable": True,
    "application": False,
    "post_init_hook": "set_other_partner_post",
}
