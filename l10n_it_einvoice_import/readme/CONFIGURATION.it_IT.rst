Devono esistere un sezionale di vendita per l'azienda e un conto credito per il
cliente: entrambi sono letti al momento della creazione della fattura.

|menu| Contabilità > Configurazione > Impostazioni

 - *Termine di pagamento cliente*: indica se il termine di pagamento della
   fattura importata viene dal file XML oppure da quello assegnato
   nell'anagrafica del cliente (predefinito)
 - *Ricerca prodotto cliente*: come cercare il prodotto — per codice interno,
   per nome esatto o per nome simile
 - *Codice IVA arrotondamento vendite*: codice IVA di vendita ad aliquota zero
   usato nella riga di arrotondamento, quando i totali del file XML non
   coincidono con quelli calcolati da Odoo. Se non impostato si usa il codice
   IVA di arrotondamento acquisti di ``l10n_it_einvoice_in``

Le prime due impostazioni possono essere ridefinite per singolo cliente,
nella scheda anagrafica.

Per vedere il numero forzato sulla scheda della fattura, l'utente deve
appartenere al gruppo *Permetti di forzare il numero fattura* di
``account_invoice_force_number``: il numero viene comunque scritto
dall'importazione, il gruppo rende soltanto visibile il campo.

Attenzione: una fattura con numero forzato non può essere cancellata, nemmeno
se ancora in bozza; è il comportamento standard di Odoo per ogni fattura a cui
sia stato assegnato un numero. Va invece annullata.
