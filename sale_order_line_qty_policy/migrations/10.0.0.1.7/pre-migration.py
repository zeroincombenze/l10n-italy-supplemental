# -*- coding: utf-8 -*-
#
# Copyright 2026 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
"""Convert auto_line_invoiced from boolean to selection, keeping its values.

Odoo cannot convert a boolean column to varchar: it renames the old column
and creates an empty one, so every product configured by hand would lose
its policy - the very loss this module already suffered once, see CLAUDE.md.
The column is converted here, in place, before the registry is loaded: Odoo
then finds a varchar column and leaves it alone.
"""


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """SELECT data_type FROM information_schema.columns
           WHERE table_name = 'product_template'
             AND column_name = 'auto_line_invoiced'""")
    row = cr.fetchone()
    if not row or row[0] != "boolean":
        return
    cr.execute(
        """ALTER TABLE product_template
           ALTER COLUMN auto_line_invoiced DROP DEFAULT,
           ALTER COLUMN auto_line_invoiced TYPE varchar
           USING CASE WHEN auto_line_invoiced THEN 'always' ELSE 'never' END""")
