When an invoice is create, the flag "To send mail" is set or reset based on
configuration values. This value can be updated by user.

When cron action starts, it sends mail for all invoices which have flag "To send mail"
set to true. After invoice pdf is sent, the flag is reset.
