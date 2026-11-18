from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from .access_compat import ensure_read_access


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def mobile_get_product_price(
        self, pricelist_id, product_id, quantity=1.0, date=None
    ):
        """通过外部 API 返回一个商品的 Odoo 标准价格。

        外部 API 不能传输 ORM 记录集。此公开包装方法接收 ID、检查标准读取
        权限，再交由 Odoo 17/18/19 标准价格表引擎计算。
        """
        try:
            pricelist_id = int(pricelist_id)
            product_id = int(product_id)
            quantity = float(quantity)
        except (TypeError, ValueError):
            raise ValidationError(_("必须提供有效的价格表、商品和数量。"))
        if pricelist_id <= 0 or product_id <= 0 or quantity <= 0:
            raise ValidationError(_("价格表、商品和数量必须大于零。"))

        pricelist = self.browse(pricelist_id).exists()
        product = self.env["product.product"].browse(product_id).exists()
        if not pricelist or not product:
            raise ValidationError(_("所选价格表或商品已不存在。"))

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
