[![Build Status](https://travis-ci.org/zeroincombenze/l10n-italy.svg?branch=8.0)](https://travis-ci.org/zeroincombenze/l10n-italy)
[![license agpl](https://img.shields.io/badge/licence-AGPL--3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0.html)
[![Coverage Status](https://coveralls.io/repos/github/zeroincombenze/l10n-italy/badge.svg?branch=8.0)](https://coveralls.io/github/zeroincombenze/l10n-italy?branch=8.0)
[![codecov](https://codecov.io/gh/zeroincombenze/l10n-italy/branch/8.0/graph/badge.svg)](https://codecov.io/gh/zeroincombenze/l10n-italy/branch/8.0)
[![OCA_project](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-oca-8.svg)](https://github.com/OCA/l10n-italy/tree/8.0)
[![Tech Doc](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-docs-8.svg)](http://wiki.zeroincombenze.org/en/Odoo/8.0/dev)
[![Help](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-help-8.svg)](http://wiki.zeroincombenze.org/en/Odoo/8.0/man/FI)
[![try it](http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-8.svg)](http://erp8.zeroincombenze.it)


[![en](https://github.com/zeroincombenze/grymb/blob/master/flags/en_US.png)](https://www.facebook.com/groups/openerp.italia/)

[![icon](static/src/img/icon.png)](https://travis-ci.org/zeroincombenze)

Stock parzial move
==================

This module permits splitting of a picking in more pickings just diminishing
the number of products, when create a delivery from Sale Order.



[![it](https://github.com/zeroincombenze/grymb/blob/master/flags/it_IT.png)](https://www.facebook.com/groups/openerp.italia/)

Movimentazione parziale stock
=============================

Questo modulo permette di di dividere una consegna in più parti, diminuendo
il numero dei prodotti quando si crea da ordine di vendita.


### Funzionalità & Certificati

Funzione | Status | Note
--- | --- | ---
Consegne da ordini di vendita | :white_check_mark: | Consegna parziale
Consegne da ordini di vendita | :white_check_mark: | Consegna parziale con chiusura


Installation
------------

These instruction are just an example to remember what you have to do:

    git clone https://github.com/zeroincombenze/l10n-italy-supplemental
    for module in stock_parzial_move; do
        mv ODOO_DIR/l10n-italy/$module BACKUP_DIR/
        cp -R l10n-italy/$module ODOO_DIR/l10n-italy/
    sudo service odoo-server restart -i stock_parzial_move -d MYDB

From UI: go to Setup > Module > Install


Configuration
-------------


Usage
-----

For furthermore information, please visit http://wiki.zeroincombenze.org/it/Odoo/7.0/man/FI


Known issues / Roadmap
----------------------


Bug Tracker
-----------

Have a bug? Please visit https://odoo-italia.org/index.php/kunena/home


Credits
-------

### Contributors

* Andrei Levin <andrei.levin@didotech.com>

### Funders

This module has been financially supported by

* Didotech srl <http://www.didotech.com>

### Maintainer

[![Odoo Italia Associazione](https://www.odoo-italia.org/images/Immagini/Odoo%20Italia%20-%20126x56.png)](https://odoo-italia.org)

Odoo Italia is a nonprofit organization whose develops Italian Localization for
Odoo.

To contribute to this module, please visit <https://odoo-italia.org/>.


[//]: # (copyright)

----

**Odoo** is a trademark of [Odoo S.A.](https://www.odoo.com/) (formerly OpenERP, formerly TinyERP)

**OCA**, or the [Odoo Community Association](http://odoo-community.org/), is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

**zeroincombenze®** is a trademark of [SHS-AV s.r.l.](http://www.shs-av.com/)
which distributes and promotes **Odoo** ready-to-use on its own cloud infrastructure.
[Zeroincombenze® distribution](http://wiki.zeroincombenze.org/en/Odoo)
is mainly designed for Italian law and markeplace.
Everytime, every Odoo DB and customized code can be deployed on local server too.

[//]: # (end copyright)

[//]: # (addons)

[//]: # (end addons)

[![chat with us](https://www.shs-av.com/wp-content/chat_with_us.gif)](https://tawk.to/85d4f6e06e68dd4e358797643fe5ee67540e408b)






\[!\[license
agpl\](<https://img.shields.io/badge/licence-AGPL--3-blue.svg>)\](<http://www.gnu.org/licenses/agpl-3.0.html>)
\[!\[Coverage
Status\](<https://coveralls.io/repos/OCA/l10n-italy-supplemental/badge.svg?branch=8.0>)\](<https://coveralls.io/OCA_txt2repos/OCA/l10n-italy-supplemental?branch=8.0>)
\[!\[codecov\](<https://codecov.io/gh/OCA/l10n-italy-supplemental/branch/8.0/graph/badge.svg>)\](<https://codecov.io/gh/OCA/l10n-italy-supplemental/branch/8.0>)
\[!\[try
it\](<http://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-8.svg>)\](<http://erp8.zeroincombenze.it>)

Description

This module permits splitting of a picking in more pickings just
diminishing the number of products.

\[//\]: \# (copyright)

------------------------------------------------------------------------

**Odoo** is a trademark of \[Odoo S.A.\](<https://www.odoo.com/>)
(formerly OpenERP, formerly TinyERP)

**OCA**, or the \[Odoo Community
Association\](<http://odoo-community.org/>), is a nonprofit organization
whose mission is to support the collaborative development of Odoo
features and promote its widespread use.

**zeroincombenze®** is a trademark of \[SHS-AV
s.r.l.\](<http://www.shs-av.com/>) which distributes and promotes
**Odoo** ready-to-use on its own cloud infrastructure. \[Zeroincombenze®
distribution\](<http://wiki.zeroincombenze.org/en/Odoo>) is mainly
designed for Italian law and markeplace. Everytime, every Odoo DB and
customized code can be deployed on local server too.

\[//\]: \# (end copyright)

\[//\]: \# (addons)

\[//\]: \# (end addons)
