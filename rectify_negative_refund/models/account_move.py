from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def rectify_invoice(self):
        """Flip an invoice/bill whose total is negative into its matching
        credit note/refund, negating its lines.

        Ported from `account.invoice` (merged into `account.move` since
        13.0): `type` -> `move_type`, `open` state -> `posted`,
        `action_invoice_cancel/draft/open` -> `button_cancel`/
        `button_draft`/`action_post`. The raw-SQL updates on a
        posted/locked record are kept as close to the original as
        practical, now against the `account_move` table.

        `fatturapa_attachment_out_id`/`fatturapa_state` came from the
        (pre-13.0) l10n_it_fatturapa module and were never declared as a
        dependency of this module even originally; guarded with
        `hasattr` so this degrades gracefully if that module (or a
        successor with different field names, e.g. l10n_it_edi) isn't
        installed.
        """
        ctr = 0
        for move in self:
            if move.move_type.startswith("in_") and move.check_total < 0.0:
                self.env.cr.execute(
                    "UPDATE account_move"
                    " SET move_type='in_refund'"
                    ", check_total=%s"
                    " WHERE id=%s",
                    (-move.check_total, move.id),
                )
                ctr = 1
                continue

            saved_state = move.state
            new_move_type = move.move_type
            if "_invoice" in move.move_type:
                new_move_type = move.move_type.replace("_invoice", "_refund")
            saved_attachment_id = False
            saved_fatturapa_state = False
            has_fatturapa = hasattr(move, "fatturapa_attachment_out_id")
            if move.state == "posted":
                if has_fatturapa:
                    saved_attachment_id = move.fatturapa_attachment_out_id
                    saved_fatturapa_state = move.fatturapa_state
                    if saved_attachment_id:
                        # We use SQL because the move is locked
                        self.env.cr.execute(
                            "UPDATE account_move"
                            " SET fatturapa_attachment_out_id=null"
                            ", fatturapa_state=null"
                            " WHERE id=%s",
                            (move.id,),
                        )
                        # Invalidate cache and reload move updated by SQL
                        self.env.invalidate_all()
                        move = self.env["account.move"].browse(move.id)
                move.button_cancel()
                move.button_draft()
            if move.state != "draft":
                continue
            if move.move_type != new_move_type:
                move.move_type = new_move_type
            # Negate every regular (non-tax/section/note) line. There is
            # no public `compute_taxes()` anymore (removed with
            # account.invoice); wrap the batch of line writes in the
            # core `_get_edi_creation` helper so tax lines and totals -
            # which the ORM does not recompute automatically for
            # non-stored dynamic lines - are resynced once, after every
            # line has been changed.
            with move._get_edi_creation() as move:
                for line in move.invoice_line_ids:
                    line.price_unit = -line.price_unit
            ctr = 1
            if saved_state == "posted":
                move.action_post()
                if has_fatturapa and saved_attachment_id:
                    # Avoid account check, so we force restoring via SQL
                    self.env.cr.execute(
                        "UPDATE account_move"
                        " SET fatturapa_attachment_out_id=%s"
                        ", fatturapa_state=%s"
                        " WHERE id=%s",
                        (saved_attachment_id, saved_fatturapa_state, move.id),
                    )
        if ctr == 0:
            return False

    def rectify_entry(self):
        pass
