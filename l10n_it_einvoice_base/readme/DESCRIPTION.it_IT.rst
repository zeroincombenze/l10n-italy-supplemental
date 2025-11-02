Questo modulo gestisce l'infrastruttura per generare il file xml della Fattura
Elettronica e della FatturaPA, versione 1.2.1, da trasmettere al sistema di
interscambio SdI.

In anagrafica clienti i dati per la fattura elettronica sono inseribili nella
scheda "Agenzia delle Entrate".


Destinatari
-----------

Il modulo è destinato a tutte le aziende che dal 2019 emettono fattura elettronica

Normativa
---------

Le leggi inerenti la fattura elettronica sono numerose. Potete consultare
la `normativa fattura elettronica <https://www.agenziaentrate.gov.it/portale/normativa-prassi-e-regole-tecniche-fatture-elettroniche>`__


Fattura elettronica a soggetto IVA
----------------------------------

Installare il modulo *l10n_it_einvoice_out*

Si tratta della casistica più comune. Selezionare "Soggetto a fattura elettronica"
e compilare il "Codice destinatario" o la "PEC".
La partita IVA è un dato obligatorio ai fini dell'invio.
L'eventuale invio di una fattura in formato PDF è una fattura di cortesia e non
ha valore legale.

Fattura elettronica a PA
------------------------

Installare il modulo *l10n_it_einvoice_out*

Questa casistica è attiva già dal 2016. Impostare "Pubblica Amministrazione"
e compilare il "Codice ufficio". Prestare attenzione alla normativa sulla scissione dei
pagamenti e all'inserimento dei dati aggiuntivi CIG e CUP.

Fattura elettronica da DdT (TD24)
---------------------------------

Installare il modulo *l10n_it_einvoice_ddt*

Fattura elettronica a privato senza partita IVA
-----------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

La legge non prevede l'obbligo di emissione della fattura elettronica ma è
ammessa l'emissione a condizione che venga inviata una fattura in formato PDF
al cliente. Inserire il valore "0000000" nel codice destinatario e il codice fiscale.


Fattura elettronica a soggetto IVA senza Codice Destinatario ne PEC
-------------------------------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Casistica in cui un cliente con partita IVA che non abbia fornito
ne il proprio Codice Destinatario ne la propria PEC. Si riconduce al caso
precedente, inserendo il valore "0000000" nel codice destinatario ed il
codice fiscale. Anche in questo caso è obbligatorio inviare una fattura in
formato PDF al cliente.

Fattura elettronica a rappresentante fiscale in Italia
------------------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Casistica di aziende estere con rappresentanza fiscale in Italia.
Inserire nei contatti un indirizzo di fatturazione di tipo "Rappresentante fiscale"
con la partita IVA italiana ed i dati per la fatturazione elettronica.
La fattura va emessa al rappresentante fiscale.

Fattura elettronica a stabile organizzazione
--------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Casistica di aziende estere con stabile organizzazione in Italia.
Inserire nei contatti un indirizzo di fatturazione di tipo "Stabile organizzazione"
con la partita IVA italiana ed i dati per la fatturazione elettronica.
La fattura va emessa alla stabile organizzazione.

Fattura elettronica a soggetto estero
-------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Inserire il valore XXXXXXX nel codice destinatario. Il file XML viene generato
con le opportune correzioni per la validazioni dell'Agenzia delle Entrate.
Anche in questo caso è obbligatorio inviare una fattura in formato PDF al cliente.

Se il soggetto non ha ne partita IVA ne codice fiscale, nella fattura elettronica
viene inserita una partita IVA convenzionale "%(iso)s99999999999" con il codice ISO
della nazione cliente e 11 cifre '9'.

Il campo CAP viene convenzionalmente compilato con "00000" e la provincia con "EE".

Emissione fattura con dichiarazione di intento
----------------------------------------------

Installare il modulo *l10n_it_einvoice_li*

Inserire il riferimento della lettera di intento.


Emissione auto-fattura
----------------------

Casistica per fatture ricevute in regime di reverse charge (tipi documento da TD16 a
TD19) oppure per emissione auto-fatture per integrazione (TD20, TD21, TD25, TD27 e
TD28). Per l'emissione delle autofatture in regime di reverse charge, installare il
modulo *l10n_it_einvoice_out_rc* mentre l'emissione di auto-fatture in integrazione
installare il modulo *l10n_it_einvoice_out*
