This module allows to specify some fiscal dates on invoices.

Date field list:

* standard Odoo date is called registration date (both sale and purchase invoices)
* date_apply_balance is new field to declare when record is evaluated in balance sheet

Notes:

* This software is like account_invoice_entry_date module of Italian OCA group
* Italian OCA module use a new field called registration_date while this module uses tha standard Odoo "date" field
* On purchase journal, date is free, without checks
* On sale journal, date is the same of invoice_date and it is read-only
* Above rule may be disableb by journal configuration
* default value of date_apply_balance is the same of the date; end-user can update the field

