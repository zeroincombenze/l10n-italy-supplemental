Questo modulo crea le **fatture di vendita** a partire dai file XML di fattura
elettronica (FatturaPA versione 1.2.1), lo stesso lavoro che
``l10n_it_einvoice_in`` svolge per le fatture di acquisto.

È pensato per le fatture di vendita emesse fuori da Odoo — prodotte da un
altro programma, oppure riscaricate dal Sistema di Interscambio (SdI) o
dall'intermediario — che devono essere registrate in contabilità.

Nel file XML l'azienda è il *CedentePrestatore* e il cliente è il
*CessionarioCommittente*: esattamente l'opposto di una fattura ricevuta. Un
file il cui *CedentePrestatore* non è l'azienda corrente viene rifiutato.

Per ogni cliente è possibile impostare il 'Livello di dettaglio e-fattura':

 - Livello minimo: la fattura è creata senza righe; l'utente dovrà crearle in
   base a quanto indicato nella fattura elettronica
 - Livello aliquote: le righe sono cumulate per codice IVA
 - Livello massimo: ogni riga contenuta nella fattura elettronica genera una
   riga di fattura

I prodotti sono ricercati per codice interno o per descrizione, dato che una
e-fattura di vendita riporta i codici dell'azienda stessa. Se non viene
trovato alcun prodotto si usa il 'Prodotto predefinito e-fattura' del cliente.

Sono importate anche le autofatture (TipoDocumento da TD16 a TD23), ma i ruoli
nella loro testata sono invertiti: la fattura risultante viene segnalata tra le
incongruenze, così da poter essere verificata a mano.

È possibile caricare in una sola volta un intero file ZIP di fatture
elettroniche, come fa ``l10n_it_einvoice_import_zip`` per i file di acquisto;
quel modulo resta dedicato agli acquisti, così nessuno dei due deve dipendere
dall'altro.
