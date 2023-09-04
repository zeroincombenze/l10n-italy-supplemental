Import a Excel file into bank statement

Excel file must have following structure:


+----------------+------------+------+------+--------+--------+---------------+
| Data contabile | Valuta     | Dare | Avere| Divisa | Causale| Descrizione   |
+----------------+------------+------+------+--------+--------+---------------+
| 01/01/2022     | 01/01/2022 |      |  100 | EUR    | XX     | DEPOSITO      |
+----------------+------------+------+------+--------+--------+---------------+
| 10/01/2022     | 10/01/2022 |  -50 |      | EUR    | 26     | BONIFICO SEPA |
+----------------+------------+------+------+--------+--------+---------------+

You can find Excel example in example directory.
