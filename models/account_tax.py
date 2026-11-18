import math

from odoo import api, models, _
from odoo.exceptions import AccessError, ValidationError

from .access_compat import ensure_read_access


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def mobile_compute_all(
        self,
        tax_ids,
        price_unit,
        currency_id,
        quantity=1.0,
        product_id=None,
        partner_id=None,
        company_id=None,
        is_refund=False,
    ):
        """Call Odoo's standard tax engine and return JSON-safe results."""
        try:
            tax_ids = [int(tax_id) for tax_id in tax_ids]
            currency_id = int(currency_id)
            price_unit = float(price_unit)
            quantity = float(quantity)
            company_id = int(company_id)
            product_id = int(product_id) if product_id else False
            partner_id = int(partner_id) if partner_id else False
        except (TypeError, ValueError):
            raise ValidationError(
                _("Invalid taxes, amount, currency, or company parameters.")
            )

        if not math.isfinite(price_unit) or not math.isfinite(quantity):
            raise ValidationError(_("Amount and quantity must be finite numbers."))
        if not isinstance(is_refund, bool):
            raise ValidationError(_("The refund flag must be a boolean."))

        if not tax_ids or any(tax_id <= 0 for tax_id in tax_ids):
            raise ValidationError(_("At least one valid tax ID is required."))
        if currency_id <= 0 or company_id <= 0:
            raise ValidationError(_("Valid currency and company IDs are required."))

        company = self.env["res.company"].browse(company_id).exists()
        if not company or company_id not in self.env.companies.ids:
            raise AccessError(
                _("You are not allowed to calculate taxes for the selected company.")
            )
        ensure_read_access(company)

        currency = self.env["res.currency"].browse(currency_id).exists()
        if not currency:
            raise ValidationError(_("The selected currency does not exist."))
        ensure_read_access(currency)

        taxes = self.browse(tax_ids).exists()
        if len(taxes) != len(set(tax_ids)):
            raise ValidationError(_("One or more tax records do not exist."))
        ensure_read_access(taxes)
        if any(tax.company_id not in company._accessible_branches() for tax in taxes):
            raise AccessError(
                _(
                    "The selected taxes do not belong to the selected company "
                    "or its accessible branches."
                )
            )

        product = (
            self.env["product.product"].browse(product_id).exists()
            if product_id
            else self.env["product.product"]
        )
        if product_id and not product:
            raise ValidationError(_("The selected product variant does not exist."))
        if product:
            ensure_read_access(product)
            if (
                product.company_id
                and product.company_id not in company._accessible_branches()
            ):
                raise AccessError(
                    _(
                        "The selected product does not belong to the selected "
                        "company or its accessible branches."
                    )
                )

        partner = (
            self.env["res.partner"].browse(partner_id).exists()
            if partner_id
            else self.env["res.partner"]
        )
        if partner_id and not partner:
            raise ValidationError(_("The selected customer does not exist."))
        if partner:
            ensure_read_access(partner)

        result = taxes.with_company(company).compute_all(
            price_unit,
            currency=currency,
            quantity=quantity,
            product=product,
            partner=partner,
            is_refund=bool(is_refund),
        )
        safe_taxes = []
        for tax in result.get("taxes", []):
            safe_taxes.append({
                key: tax.get(key)
                for key in (
                    "id",
                    "name",
                    "amount",
                    "base",
                    "sequence",
                    "price_include",
                    "is_reverse_charge",
                )
            })
        return {
            "total_excluded": result["total_excluded"],
            "total_included": result["total_included"],
            "taxes": safe_taxes,
        }
