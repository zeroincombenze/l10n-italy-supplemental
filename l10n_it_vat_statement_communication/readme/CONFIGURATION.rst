In order to generate VAT statement's periods,
open Accounting > Configuration > Date ranges > Generate Date Ranges and select:

* range name prefix: prefix identifying the periods to be generated (usually the year)
* duration: 1 month
* number of ranges to generate: 12
* type: create a type or use an existing one, no specific configuration is required
* date start: first day of the first period to be generated (usually the first day of the year e.g. 01/01/2018)

In order to load the correct amount from tax, the tax has to be
associated to the account involved in the statement:

* open a tax in Accounting > Configuration > Accounting > Taxes,
* in the tab 'Advanced Options' select the correct account (for instance the account debit VAT)
  for the field 'Account used for VAT statement'.

If you need to calculate interest, you can add default information in your
company data (percentage and account), in the 'VAT statement' tab.
