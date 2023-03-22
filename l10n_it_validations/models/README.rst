
|Build Status| |Codecov Status| |license gpl| |Try Me|


.. contents::


Overview / Panoramica
=====================

|en| N/A

|it| N/D
Avaiable Addons / Moduli disponibili
------------------------------------

+--+------------+------------+----------------------------------------------------------------------------------+
|  | Version    | OCA Ver.   | Description / Descrizione                                                        |
+--+------------+------------+----------------------------------------------------------------------------------+



OCA comparation / Confronto con OCA
-----------------------------------


+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Description / Descrizione                                       | Zeroincombenze    | OCA            | Notes / Note                   |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+
| Coverage / Copertura test                                       |  |Codecov Status| | |OCA Codecov|  |                                |
+-----------------------------------------------------------------+-------------------+----------------+--------------------------------+



Getting started / Come iniziare
===============================

|Try Me|


Prerequisites / Prerequisiti
----------------------------


* python 3.7+
* postgresql 9.5+ (experimental 10.0+)


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
    odoo_install_repository models -b 12.0 -O powerp -o $HOME/12.0
    vem create $HOME/12.0/venv_odoo -O 12.0 -a "*" -DI -o $HOME/12.0



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
    odoo_install_repository models -b 12.0 -o $HOME/12.0 -U
    vem amend $HOME/12.0/venv_odoo -o $HOME/12.0
    # Adjust following statements as per your system
    sudo systemctl restart odoo



Get involved / Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/powerp/models/issues>`_.

In case of trouble, please check there if your issue has already been reported.

Credits / Didascalie
====================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


----------------


|en| **Powerp** is the Italian Enterprises Network born in 2020, whose mission is promote use of Odoo to cover Italian law and markeplace.

`Powerp <http://www.powerp.it/>`__ distributes code under `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ or `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__ licenses.

Read carefully published README for more info about authors.

|it| `Powerp <http://www.powerp.it/>`__ è una rete di imprese, nata nel 2020 che rilascia moduli per la localizzazione italiana evoluta.

`Powerp <http://www.powerp.it/>`__ distribuisce il codice con licenze `LGPL <https://www.gnu.org/licenses/lgpl-3.0.html>`__ e `OPL <https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html>`__

I soci fondatori sono:

* `Didotech s.r.l. <http://www.didotech.com>`__
* `SHS-AV s.r.l. <https://www.shs-av.com/>`__
* `Xplain s.r.l. <http://x-plain.it//>`__

Leggere con attenzione i file README per maggiori informazioni sugli autori.


|chat_with_us|


|


Last Update / Ultimo aggiornamento: 2021-02-15

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: Alfa
.. |Build Status| image:: https://travis-ci.org/powerp/models.svg?branch=12.0
    :target: https://travis-ci.org/powerp/models
    :alt: github.com
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/9.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Coverage Status| image:: https://coveralls.io/repos/github/powerp/models/badge.svg?branch=12.0
    :target: https://coveralls.io/github/powerp/models?branch=12.0
    :alt: Coverage
.. |Codecov Status| image:: https://codecov.io/gh/powerp/models/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/powerp/models/branch/12.0
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
.. |OCA Codecov| image:: https://codecov.io/gh/OCA/models/branch/12.0/graph/badge.svg
    :target: https://codecov.io/gh/OCA/models/branch/12.0
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
   :target: https://t.me/axitec_helpdesk

