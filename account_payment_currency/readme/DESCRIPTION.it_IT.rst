Questo modulo estende il form di pagamento (``account.payment``) per
mostrare l'importo del pagamento convertito nella valuta contabile
dell'azienda, accanto all'importo espresso nella valuta del pagamento
stesso.

È utile quando si registra un pagamento in una valuta diversa da quella
contabile dell'azienda: il modulo cerca automaticamente il tasso di cambio
in vigore alla data del pagamento e calcola l'importo equivalente nella
valuta aziendale, in modo che l'utente possa verificarlo a colpo d'occhio
senza uscire dal form di pagamento.
