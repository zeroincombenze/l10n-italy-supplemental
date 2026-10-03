When registering a payment (from an invoice or from the *Payments* menu),
two extra fields appear next to the payment journal, visible only to users
belonging to the *Multi-Currency* group:

* **Company Currency Payment Amount**: the payment amount converted into
  the company's accounting currency.
* **Company Currency**: the company's accounting currency, shown for
  reference.

The converted amount is recalculated automatically whenever the payment
amount, currency, payment date or journal changes:

* if the payment journal's currency matches the currency of the invoice(s)
  being paid, the amount due in company currency is simply summed from the
  invoices, with no conversion;
* otherwise, the amount is converted using the exchange rate in effect on
  the payment date.

Paying several invoices in different currencies with the same payment is
not supported and raises an error.
