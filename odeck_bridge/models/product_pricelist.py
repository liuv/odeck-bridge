from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from .access_compat import ensure_read_access


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def mobile_get_product_price(
        self, pricelist_id, product_id, quantity=1.0, date=None
    ):
        """Return an Odoo-calculated product price through the external API.

        The API accepts record IDs rather than ORM recordsets, checks read access,
        and delegates calculation to Odoo's standard pricelist engine.
        """
        try:
            pricelist_id = int(pricelist_id)
            product_id = int(product_id)
            quantity = float(quantity)
        except (TypeError, ValueError):
            raise ValidationError(
                _("A valid pricelist, product, and quantity are required.")
            )
        if pricelist_id <= 0 or product_id <= 0 or quantity <= 0:
            raise ValidationError(
                _("Pricelist, product, and quantity must be greater than zero.")
            )

        pricelist = self.browse(pricelist_id).exists()
        product = self.env["product.product"].browse(product_id).exists()
        if not pricelist or not product:
            raise ValidationError(
                _("The selected pricelist or product no longer exists.")
            )

        ensure_read_access(pricelist)
        ensure_read_access(product)
        pricelist.ensure_one()
        product.ensure_one()

        price_date = (
            fields.Date.to_date(date) if date else fields.Date.context_today(self)
        )
        company = pricelist.company_id or self.env.company
        pricelist = pricelist.with_company(company)
        price, rule = pricelist._get_product_price_rule(
            product,
            quantity=quantity,
            uom=product.uom_id,
            date=price_date,
            currency=pricelist.currency_id,
        )
        return {
            "price": price,
            "rule_id": rule or False,
            "pricelist_id": pricelist.id,
            "product_id": product.id,
            "currency_id": pricelist.currency_id.id,
            "date": fields.Date.to_string(price_date),
        }
