When you start with a new Odoo installation, you would need to record customers and
suppliers account opening entries with balance from previus database.

This module write account entries with partner balance for account opening from
Excel file.

Excel file must have following structure:

+---------+-------------------------+----------+-----------+-------------------+------+--------+
| Codice  | Nome                    | Cliente  | Fornitore | Partita IVA       | Dare | Avere  |
+---------+-------------------------+----------+-----------+-------------------+------+--------+
|         | Global Trading Ltd      | 1        |           | GB250072348000    | 1000 |        |
+---------+-------------------------+----------+-----------+-------------------+------+--------+
|         | Rossi e Bianchi srl     |          | 1         | IT05111810015     |      | 500    |
+---------+-------------------------+----------+-----------+-------------------+------+--------+
| 180003  | Banca                   |          |           |                   | 100  |        |
+---------+-------------------------+----------+-----------+-------------------+------+--------+



Notes:

* Please, import just xlsx files
* The labels of the header must be exactly as you see above
* Partners are searched by vat code and name
* Ref field is not required; use it if you want load partner by code

You can find Excel example in example directory.
