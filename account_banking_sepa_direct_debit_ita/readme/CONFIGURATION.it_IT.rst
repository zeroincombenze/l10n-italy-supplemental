* Azienda: impostare il **Codice Identificativo del Creditore** e
  l'**Identificativo della parte iniziante**, cioè il codice univoco CBI
  (CUC, 8 lettere o cifre). Entrambi possono essere ridefiniti nel modo di pagamento.
* Registro banca: aggiungere il metodo *Sepa Direct Debit CORE ITA-CBI*
  o *Sepa Direct Debit B2B ITA-CBI* ai pagamenti in entrata.
* Modo di pagamento: creare un modo con uno dei metodi sopra e il registro banca.
* Cliente: il conto bancario deve avere un IBAN valido e la banca il codice BIC;
  creare un mandato valido con lo stesso schema (CORE o B2B) del metodo.

Se è installato un modulo che gestisce i conti di portafoglio, nel file viene
scritto come creditore il conto principale del portafoglio.
