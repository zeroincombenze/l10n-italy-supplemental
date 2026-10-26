SEPA Direct Debit file in the Italian CBI format
------------------------------------------------

Italian banks accept SEPA Direct Debit collections in the CBI format
(``CBISDDReqLogMsg``) instead of the standard ISO 20022 pain.008 file.
This module adds two payment methods to the OCA payment orders:

* **Sepa Direct Debit CORE ITA-CBI**: debits to consumers (CORE scheme)
* **Sepa Direct Debit B2B ITA-CBI**: debits to businesses (B2B scheme)

A debit payment order using one of these methods generates the CBI file,
ready to be uploaded to the home banking.

The file is created by the Python library ``fintech``.
