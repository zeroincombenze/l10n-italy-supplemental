### document_2c_fatturapa.py
Continene la classe FatturaPA_2C che effettua la comunicazione con 2C.
Invio fattura ha 2 step:
    1. FatturaPA_2C.upload_data: caricamento della fattura in 2C
    2. send_fatturapa: dice a 2C di inviare la fattura precedentemente caricata a SdI


### inherit_res_company.py
Aggiunta campi per configurazione comunicazione 2C con relativa form di inserimento


### inherit_fatturapa_attachment_out.py
Estende la classe fatturapa.attachment.out per la gestione dell'invio fatturaPA.
Invio da 2C.
Aggiornamento dello stato di invio e controllo dei messaggi da SdI tramite cron


### CRON
Dopo l'invio il cron controlla le fatturapa_attachment_out con state == 'sent' o 'RC' e chiama l'API 2C
GetElectronicInvoiceOutcomes e segna con il messaggio di ritorno da 2C/SdI

Inoltre una volta al giorno vengono inviate tutte le fatture elettroniche create ma non ancora inviate allo SDI
