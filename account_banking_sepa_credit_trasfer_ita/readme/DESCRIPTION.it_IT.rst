File bonifici SEPA nel formato CBI italiano
-------------------------------------------

Le banche italiane accettano i bonifici SEPA nel formato CBI
(``CBIPaymentRequest.00.04.00``) invece del file standard ISO 20022 pain.001.
Questo modulo aggiunge il metodo di pagamento **Sepa Credit Transfer ITA CBI**
alle distinte di pagamento OCA: una distinta con questo metodo genera il file CBI,
pronto per essere caricato sull'home banking.

Il file è creato dalla libreria Python ``fintech``.
