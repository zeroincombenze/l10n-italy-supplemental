This module extends the payment form (``account.payment``) to show the
payment amount converted into the company's accounting currency, alongside
the amount expressed in the payment's own currency.

It is useful when registering a payment in a currency that differs from the
company's accounting currency: the module automatically looks up the
exchange rate in effect on the payment date and computes the equivalent
amount in the company currency, so the user can verify it at a glance
without leaving the payment form.
