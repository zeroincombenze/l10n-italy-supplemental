Quando parte una nuova installazione di Odoo è necessario caricare i saldi contabili
dei clienti e fornitori.

Questo modulo registra le operazioni contabili di apertura clienti e fornitori da
un file Excel.

Il file Excel ha la seguente struttura:

+---------+-------------------------+----------+-----------+-------------------+------+--------+
| Codice  | Nome                    | Cliente  | Fornitore | Partita IVA       | Dare | Avere  |
+---------+-------------------------+----------+-----------+-------------------+------+--------+
|         | Global Trading Ltd      | 1        |           | GB250072348000    | 1000 |        |
+---------+-------------------------+----------+-----------+-------------------+------+--------+
|         | Rossi e Bianchi srl     |          | 1         | IT05111810015     |      | 500    |
+---------+-------------------------+----------+-----------+-------------------+------+--------+
| 180003  | Banca                   |          |           |                   | 100  |        |
+---------+-------------------------+----------+-----------+-------------------+------+--------+



Note:

* Si possono importare solo file .xlsx
* Le etichette dell'intestazione devono essere rispettate
* Sono cercati per partita IVA o codice fiscale e nome simile
* Il campo Ref è facoltativo; serve se evantuali ricerche per codice

Si può vedere un esempio nella cartella example.
