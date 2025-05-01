#
from odoo import api, models


class BaseModel(models.BaseModel):

    _inherit = "base"

    @api.model
    def ancestor_value(self, match, value=None, field=None, skip_current=False):
        """Return the ancestor value from current record by a field value

        Args:
            match (str): Field name to match with value or not zero
                         magic value "self" matches the complete record with value.
            value (any): Value to match; if not supplied, field is matched to not zero.
            field (str): Field name to return value; same of match if not supplied;
                         magic value "self" returns the complete record.
            skip_current (bool): Skip current value if True (real ancestor value).

        Returns:
            Appropriate value
        """
        rec = self.parent_id if skip_current else self
        while rec:
            if (
                (match == "self" and rec == value)
                or (value is None and getattr(rec, match))
                or (value is not None and getattr(rec, match) == value)
            ):
                return rec if field == "self" else getattr(rec, field or match)
            rec = rec.parent_id
        return False
