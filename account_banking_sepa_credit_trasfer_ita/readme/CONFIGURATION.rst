* Company: set the **Initiating Party Identifier**, which is the CBI unique code
  (CUC, 8 letters or digits). It can be overridden on the payment mode.
* Bank journal: the bank account must be an Italian IBAN; add the payment method
  *Sepa Credit Transfer ITA CBI* to the outgoing payments.
* Payment mode: create a mode with this method and the bank journal.
* Supplier: the bank account needs a valid IBAN.

If a module providing wallet accounts ("conto di portafoglio") is installed,
the main bank account of the wallet is written in the file as debtor.
