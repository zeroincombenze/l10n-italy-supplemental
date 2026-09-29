|menu| Contabilità > Vendite > File e-fattura emesse

 - Caricare il file XML, oppure caricare un intero file ZIP da
   |menu| Contabilità > Vendite > Fattura elettronica > Import eInvoice from ZIP,
   che è il corrispondente per le vendite dello stesso menu sotto Acquisti
 - Visualizzare il contenuto del file facendo clic su "Anteprima"
 - Eseguire la procedura guidata "Importa e-fattura di vendita" per creare le
   fatture cliente in bozza nel sezionale di vendita scelto nella procedura;
   il sezionale è obbligatorio e deve appartenere all'azienda che emette la
   fattura

L'elenco mostra, per ogni file, quante fatture contiene e se sono già
registrate; il filtro *Non registrate* seleziona i file ancora da importare. Un
file importato dalla procedura viene contrassegnato come *Importato*, per
distinguerlo da quelli generati da questo sistema a partire dalle proprie
fatture.

Tutto ciò che non è stato possibile abbinare — un codice IVA, un termine di
pagamento, un prodotto — viene scritto nel campo "Incongruenze di
importazione" della fattura creata, che resta in stato bozza per la verifica.

Un file caricato qui è già stato inviato al Sistema di Interscambio da chi lo ha
prodotto, perciò viene contrassegnato come *Inviato* già al momento del
caricamento, non solo dopo l'importazione. Se restasse nello stato *Pronto per
l'invio*, la procedura oraria di invio di ``l10n_it_einvoice_send2sdi`` lo
invierebbe allo SdI una seconda volta. I file generati da questo sistema non
sono toccati e restano *Pronti per l'invio*.

Per inviare comunque un file di questo tipo, usare il pulsante *Reimposta a
pronto* sul file.

Il numero della fattura importata è quello scritto nel file XML, forzato
tramite il campo *Forza numero* di ``account_invoice_force_number``: il
documento è già noto allo SdI e al cliente con quel numero, perciò il
sezionale di vendita non deve rinumerarlo.
