from odoo import _
from odoo.exceptions import AccessError


def ensure_read_access(records):
    """Check record and model read access across Odoo 17 through 20."""
    if hasattr(records, "has_access"):
        if not records.has_access("read"):
            raise AccessError(_("You do not have read access to these records."))
        return

    records.check_access_rights("read")
    records.check_access_rule("read")
