* Company: set the **SEPA Creditor Identifier** and the **Initiating Party
  Identifier**, which is the CBI unique code (CUC, 8 letters or digits).
  Both can be overridden on the payment mode.
* Bank journal: add the payment method *Sepa Direct Debit CORE ITA-CBI*
  or *Sepa Direct Debit B2B ITA-CBI* to the incoming payments.
* Payment mode: create a mode with one of the methods above and the bank journal.
* Customer: the bank account needs a valid IBAN and the bank a BIC code;
  create a valid mandate with the same scheme (CORE or B2B) as the method.

If a module providing wallet accounts ("conto di portafoglio") is installed,
the main bank account of the wallet is written in the file as creditor.
