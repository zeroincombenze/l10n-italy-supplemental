Cosa è
------

Questo modulo non ha funzioni specifiche per l'utente finale.
Contiene dati e definizioni come stabilito dall'Agenzia delle Entrate
All'interno sono presenti gli schemi xml usati da FatturaPA,
Fattura Elettronica B2B, Liquidazione IVA elettronica e Comunicazione IVA.

Destinatari
-----------

Tutti i soggetti passivi IVA in regime


Normativa e prassi
------------------

* `DPR 633/72 <https://www.gazzettaufficiale.it/eli/id/1972/11/11/072U0633/sg>`__
* `DL 331/93 <https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.dataPubblicazioneGazzetta=1993-12-07&amp;atto.codiceRedazionale=093A6723&amp;elenco30giorni=false>`__
* `DL 41/95 <https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.dataPubblicazioneGazzetta=1995-02-23&amp;atto.codiceRedazionale=095G0076&amp;elenco30giorni=false>`__

Tutti i moduli che generano file xml dipendenti dallo schema dell'Agenzia delle Entrate
devono dichiare il modulo `l10n_it_ade <{{GIT_URL_ROOT}}/tree/{{branch}}/l10n_it_ade>`__
come dipendenza.

Questo modulo eredita alcune parti di codice dai moduli *l10n_it_account*
e *l10n_it_fiscal_document_type* di OCA.
