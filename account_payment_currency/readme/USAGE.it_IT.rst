Quando si registra un pagamento (da una fattura o dal menu *Pagamenti*),
accanto al diario di pagamento compaiono due campi aggiuntivi, visibili solo
agli utenti appartenenti al gruppo *Multi-valuta*:

* **Importo Pagamento in Valuta Aziendale**: l'importo del pagamento
  convertito nella valuta contabile dell'azienda.
* **Valuta Aziendale**: la valuta contabile dell'azienda, mostrata per
  riferimento.

L'importo convertito viene ricalcolato automaticamente ogni volta che
cambiano l'importo, la valuta, la data o il diario del pagamento:

* se la valuta del diario di pagamento coincide con quella delle fatture
  pagate, l'importo dovuto in valuta aziendale viene semplicemente sommato
  dalle fatture, senza alcuna conversione;
* in caso contrario, l'importo viene convertito utilizzando il tasso di
  cambio in vigore alla data del pagamento.

Pagare con un unico pagamento fatture con valute diverse tra loro non è
supportato e genera un errore.
