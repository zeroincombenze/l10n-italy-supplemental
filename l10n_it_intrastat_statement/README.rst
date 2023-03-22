
=======================================================
|icon| ITA - Dichiarazione Intrastat Plus 12.0.1.2.4_13
=======================================================


**Dichiarazione Intrastat Plus per l"Agenzia delle Dogane**

.. |icon| image:: https://raw.githubusercontent.com/PowERP-cloud/l10n-italy/12.0/l10n_it_intrastat_statement/static/description/icon.png

|Maturity| |Build Status| |license opl|


.. contents::



Overview / Panoramica
=====================

|en| Intrastat module extension


|

|it| Estensione del modulo Intrastat

Questo modulo si occupa di generare la dichiarazione Intrastat e le relative stampe.

Le specifiche per tali stampe e i file da inviare sono in https://www.adm.gov.it/portale/dogane/operatore/modulistica/elenchi-scambi-intracomunitari-di-beni, in particolare gli allegati XI e XII.


|

Usage / Utilizzo
----------------

**Italiano**


**Dichiarazione Intrastat**

Accedere a *Fatturazione/Contabilità → Contabilità → Intrastat → Dichiarazioni Intrastat* ed utilizzare il pulsante «Crea» per creare una nuova dichiarazione.

N.B.: il menù "Contabilità" è visibile solo se vengono abilitate le funzionalità contabili complete.

Nella parte superiore della maschera, inserire i dati:

- *Azienda*: popolato in automatico con il nome dell'azienda;
- *Partita IVA contribuente*: la partita IVA, popolata in automatico con il nome dell'azienda;
- *Data di presentazione*: popolata in automatico con la data corrente;
- *Anno*: l'anno di presentazione, scelto dal menù a tendina che visualizza gli anni fiscali configurati a sistema;
- *Tipo periodo*: l’orizzonte temporale a cui fa riferimento la dichiarazione, scelto da menù a tendina con le voci “Mese” o “Trimestre”;
- *Periodo*: il periodo temporale a cui fa riferimento la dichiarazione. Inserire il numero del mese (es. 9 per settembre, se nel campo "Tipo periodo" è stato selezionato “Mese”, oppure in numero del trimestre (es: 1 per il trimestre gennaio-marzo), se nel campo "Tipo periodo" è stato selezionato “Trimestre”;
- *Caselle di selezione “Cessioni” e “Acquisti”*: da selezionare in base alla tipologia di operazioni che si vogliono inserire nella dichiarazione;
- *Numero*: progressivo della dichiarazione proposto in automatico dal sistema;
- *Tipo di contenuto*: selezionare la voce di competenza dal menù a tendina;
- *Casi speciali*: selezionare la voce di competenza dal menù a tendina;
- *Sezione doganale*: selezionare la voce di riferimento dal menù a tendina.

Inseriti e salvati i dati, utilizzare il pulsante «Ricalcola» per popolare la dichiarazione. Per ciascuna scheda (”Cessioni” e “Acquisti”) verranno inserite nelle sezioni di riferimento:

- Cessioni:

  - Cessione beni - Sezione 1 → fatture di vendita di merci
  - Rettifica beni - Sezione 2 → note di credito su vendita merci
  - Cessione servizi - Sezione 3 → fatture di vendita di servizi
  - Rettifica servizi - Sezione 4 → note di credito su vendita servizi

- Acquisti:

  - Acquisto beni - Sezione 1 → fatture di acquisto di merci
  - Rettifica beni - Sezione 2 → note di credito su acquisto merci
  - Acquisto servizi - Sezione 3 → fatture di acquisto di servizi
  - Rettifica servizi - Sezione 4 → note di credito su acquisto servizi

I dati presi dalle fatture e dalle note di credito indicate come soggette ad Intrastat, relative al periodo di riferimento.

N.B.: i record presenti nelle schede "Rettifica beni - Sezione 2" e "Rettifica servizi - Sezione 4", sia per gli acquisti che per le vendite, vanno modificati per inserire i dati obbligatori mancanti.

Inseriti i dati e salvata la dichiarazione, è possibile procedere all’elaborazione dei file da inviare all’Agenzia delle Dogane tramite l’apposito pulsante «Esporta file». 

Il pulsante fa partire una procedura guidata, che permette di scegliere quale tipo di file estrarre:

- file di invio (complessivo)
- file acquisti.cee
- file cessioni.cee

Il file potrà essere scaricato tramite l’apposito link visualizzato nella maschera della procedura guidata. Di seguito un esempio per lo scaricamento del file cessioni.cee (il nome del file da scaricare è SCAMBI.CEE).

Dalla voce *Stampa* è possibile generare gli elenchi riepilogativi delle cessioni o degli acquisti intracomunitari: modello INTRA-1, INTRA-1 Bis, INTRA-1 Ter, INTRA-2, INTRA-2 Bis.


|

OCA comparation / Confronto con OCA
-----------------------------------


+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Description / Descrizione                                       | Zeroincombenze    | OCA            | Notes / Note                   |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Coverage / Copertura test                                       |  |Codecov Status| | |OCA Codecov|  |                                |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+


|
|

Getting started / Come iniziare
===============================

|Try Me|


|

Installation / Installazione
----------------------------


+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| These instructions are just an  | Istruzioni di esempio valide solo per    |
| example; use on Linux CentOS 7+ | distribuzioni Linux CentOS 7+,           |
| Ubuntu 14+ and Debian 8+        | Ubuntu 14+ e Debian 8+                   |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__    |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| $HOME/12.0                                                                 |
+----------------------------------------------------------------------------+

::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository installation; OCB repository must be installed
    odoo_install_repository l10n-italy -b 12.0 -O powerp -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0

From UI: go to:

* |menu| Setting > Activate Developer mode 
* |menu| Apps > Update Apps List
* |menu| Setting > Apps |right_do| Select **l10n_it_intrastat_statement** > Install


|

Upgrade / Aggiornamento
-----------------------


::

    cd $HOME
    # *** Tools installation & activation ***
    # Case 1: you have not installed zeroincombenze tools
    git clone https://github.com/zeroincombenze/tools.git
    cd $HOME/tools
    ./install_tools.sh -p
    source $HOME/devel/activate_tools
    # Case 2: you have already installed zeroincombenze tools
    cd $HOME/tools
    ./install_tools.sh -U
    source $HOME/devel/activate_tools
    # *** End of tools installation or upgrade ***
    # Odoo repository upgrade
    odoo_install_repository l10n-italy -b 12.0 -o $HOME/12.0 -U
    vem amend $HOME/12.0/venv_odoo -o $HOME/12.0
    # Adjust following statements as per your system
    sudo systemctl restart odoo

From UI: go to:

|

Support / Supporto
------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese `Powerp <http://www.powerp.it/>`__

Developer companies are / I soci sviluppatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__


|
|

Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/PowERP-cloud/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Proposals for enhancement
-------------------------


If you have a proposal to change this module, you may want to send an email to <info@powerp.it> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.


ChangeLog History / Cronologia modifiche
----------------------------------------

12.0.1.2.4_13 (2022-02-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Impostato la natura della transazione B come non obbligatoria
* [FIX] Verificato tracciato spazio per transazione B

12.0.1.2.4_11 (2022-02-23)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* [REF] Refactoring dei formati da inviare all'Agenzia Doganale

12.0.1.1.9 (2021-08-03)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Wrong year section 2 and 4 again

12.0.1.1.8 (2021-05-26)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Wrong year section 2 and 4

12.0.1.1.5 (2021-03-27)
~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] Swapped amount_euro and statistic_amount_euro

12.0.0.1.5 (2021-03-26)
~~~~~~~~~~~~~~~~~~~~~~~
* [IMP] Added statistic field

12.0.0.1.4 (2021-03-24)
~~~~~~~~~~~~~~~~~~~~~~~
* [IMP] Added report

12.0.0.1.1 (2021-03-23)
~~~~~~~~~~~~~~~~~~~~~~~
* [FIX] fix travis warning



|
|

Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)



|

Authors / Autori
----------------

* `Odoo Community Association (OCA) <https://odoo-community.org>`__
* `powERP <https://www.powerp.it>`__
* `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__
* `Didotech s.r.l. <https://www.didotech.com>`__


Contributors / Collaboratori
----------------------------

* Alessandro Camilli
* Lorenzo Battistini
* Lara Baggio <lbaggio@linkgroup.it>
* Glauco Prina <gprina@linkgroup.it>
* Sergio Zanchetta <https://github.com/primes2h>
* Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>
* Fabio Giovannelli <fabio.giovannelli@didotech.com>
* Marco Tosato <marco.tosato@didotech.com>
* Fabio Colognesi <fabio.colognesi@didotech.com>


Maintainer / Manutenzione
-------------------------


This module is maintained by the / Questo modulo è mantenuto dalla rete di imprese Powerp <http://www.powerp.it/>
Developer companies are / I soci sviluppatori sono:
* Didotech s.r.l. <http://www.didotech.com>
* SHS-AV s.r.l. <https://www.shs-av.com/>


|

----------------


|en| **Powerp** is an Italian enterprises network, whose mission is to develop high-level addons designed for Italian enterprise companies.

`Powerp <http://www.powerp.it/>`__ code adds new enhanced features to Italian localization and it released under `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ or `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__ licenses.

|it| `Powerp <http://www.powerp.it/>`__ è una rete di imprese italiane, nata con la missione di sviluppare moduli per le PMI.

Il codice di `Powerp <http://www.powerp.it/>`__ aggiunge caratteristiche evolute alla localizzazione italiana; il codice è rilasciato con licenze `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ e `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__

I soci fondatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__
* `Xplain s.r.l. <http://x-plain.it//>`__



|chat_with_us|


|

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2022-02-24

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |Build Status| image:: https://travis-ci.org/PowERP-cloud/l10n-italy.svg?branch=12.0
    :target: https://travis-ci.com/PowERP-cloud/l10n-italy
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/PowERP-cloud/l10n-italy/badge.svg?branch=12.0
    :target: https://coveralls.io/github/PowERP-cloud/l10n-italy?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/PowERP-cloud/l10n-italy/branch/12.0
    :alt: Codecov
.. |Tech Doc| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-12.svg
    :target: https://wiki.zeroincombenze.org/en/Odoo/12.0/dev
    :alt: Technical Documentation
.. |Help| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-12.svg
    :target: https://wiki.zeroincombenze.org/it/Odoo/12.0/man
    :alt: Technical Documentation
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-12.svg
    :target: https://erp12.zeroincombenze.it
    :alt: Try Me
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/l10n-italy/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/l10n-italy/branch/12.0
    :alt: Codecov
.. |Odoo Italia Associazione| image:: https://www.odoo-italia.org/images/Immagini/Odoo%20Italia%20-%20126x56.png
   :target: https://odoo-italia.org
   :alt: Odoo Italia Associazione
.. |Zeroincombenze| image:: https://avatars0.githubusercontent.com/u/6972555?s=460&v=4
   :target: https://www.zeroincombenze.it/
   :alt: Zeroincombenze
.. |en| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/en_US.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |it| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/it_IT.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/check.png
.. |no_check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/no_check.png
.. |menu| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/menu.png
.. |right_do| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/right_do.png
.. |exclamation| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/exclamation.png
.. |warning| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/warning.png
.. |same| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/same.png
.. |late| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/late.png
.. |halt| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/halt.png
.. |info| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/info.png
.. |xml_schema| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/iso/icons/xml-schema.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/iso/scope/xml-schema.md
.. |DesktopTelematico| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/DesktopTelematico.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/Desktoptelematico.md
.. |FatturaPA| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/fatturapa.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/fatturapa.md
.. |chat_with_us| image:: https://www.shs-av.com/wp-content/chat_with_us.gif
   :target: https://t.me/Assitenza_clienti_powERP

