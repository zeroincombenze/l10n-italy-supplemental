File SEPA Direct Debit nel formato CBI italiano
-----------------------------------------------

Le banche italiane accettano gli incassi SEPA Direct Debit nel formato CBI
(``CBISDDReqLogMsg``) invece del file standard ISO 20022 pain.008.
Questo modulo aggiunge due metodi di pagamento alle distinte OCA:

* **Sepa Direct Debit CORE ITA-CBI**: addebiti a consumatori (schema CORE)
* **Sepa Direct Debit B2B ITA-CBI**: addebiti a imprese (schema B2B)

Una distinta di incasso con uno di questi metodi genera il file CBI,
pronto per essere caricato sull'home banking.

Il file è creato dalla libreria Python ``fintech``.
