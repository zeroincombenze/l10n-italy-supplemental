Comunicazione IVA (ex Spesometro)
---------------------------------

Gestisce la Comunicazione periodica IVA con l'elenco delle fatture emesse e
ricevute e genera il file da inviare all'Agenzia delle Entrate.
Questo obbligo è conosciuto anche come Spesometro light 2018 e sostistuisce i
precedenti obblighi chiamati Spesometro e Spesometro 2017.

::

    Destinatari:

Tutti i soggetti IVA (con partita IVA)

::

    Normativa e prassi:

* `Art. 21 D.L. n. 78/2010 <https://www.gazzettaufficiale.it/gunewsletter/dettaglio.jsp?service=1&datagu=2010-05-31&task=dettaglio&numgu=125&redaz=010G0101&tmstp=1275551085053>`__
* `Art. 4 D.L. n. 193/2016 <https://www.gazzettaufficiale.it/eli/id/2016/10/24/16G00209/sg>`__
* `Art. 1ter D.L. n. 148/2017 <https://www.gazzettaufficiale.it/eli/id/2017/12/05/17A08254/SG>`__
* `Provvedimenti Agenzia delle entrate del 27 marzo 2017, numero 58793 <https://www.agenziaentrate.gov.it/wps/wcm/connect/4e22d9ab-2bbd-4e3f-9e60-a9a8cbf70232/PROVVEDIMENTO+PROT.+58793+DEL+27+MARZO+2017.pdf?MOD=AJPERES&CACHEID=4e22d9ab-2bbd-4e3f-9e60-a9a8cbf70232>`__
* `Info Agenzia delle Entrate <https://www.agenziaentrate.gov.it/wps/content/Nsilib/Nsi/Schede/Comunicazioni/Dati+Fatture+%28c.d.+nuovo+spesometro%29/Scheda+informativa+Dati+Fatture+c.d.+nuovo+spesometro/?page=schedecomunicazioni>`__

Note fiscali da circolare Agenzia delle Entrate su tipo documento fiscale:

* Le autofatture, per fatture non ricevute dopo 4 mesi, rif. art. 6 c.8 D.Lgs 471/97, (codice TD20) sono inserite nella comunicazione.
* Le autofatture da reverse charge nazionale (codice TD01) non sono inserite nello spesometro. Marcare il registro sezionale come registro con e-fatture.
* Le autofatture da reverse charge estero (codice TD01) non sono inserite nello spesometro. La relativa fattura d'acquisto è inserita nell'"esterometro". Marcare il registro sezionale come registro con e-fatture

|

Il software permette di operare in modalità 2017 per rigenerare eventuali file
in formato 2017. Per eseguire questa funzione, prima di avviare Odoo eseguire
la seguente istruzione:

::

     export SPESOMETRO_VERSION=2.0
