SEPA Credit Transfer file in the Italian CBI format
---------------------------------------------------

Italian banks accept SEPA Credit Transfers in the CBI format
(``CBIPaymentRequest.00.04.00``) instead of the standard ISO 20022 pain.001 file.
This module adds the payment method **Sepa Credit Transfer ITA CBI** to the OCA
payment orders: a payment order using it generates the CBI file, ready to be
uploaded to the home banking.

The file is created by the Python library ``fintech``.
