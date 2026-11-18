# Odeck Bridge

English | [简体中文](README.zh_CN.md)

Odeck Bridge is an optional Odoo addon that exposes permission-checked adapters for the standard Odoo pricelist and tax engines. It supports POS price and tax calculations used by the Odeck mobile client.

It does not add business records, customer-specific rules, license checks, activation keys, or database UUID binding. Login and ordinary inventory, sales, dashboard, and POS browsing in the mobile client use standard Odoo JSON-RPC and do not require this addon.

## Features

- Calculate a product price through an Odoo pricelist.
- Calculate transaction taxes through Odoo's standard tax engine.
- Validate access to the relevant records and company scope.
- Return JSON-safe results for the mobile client.
- Fail closed: the client stops a POS operation if a required server calculation is unavailable.

## Requirements

- Odoo 17.0, 18.0, 19.0, or 20.0, using the matching release branch.
- The standard Odoo `account` and `product` modules.
- Odoo.sh or an on-premise deployment that permits Python addons.
- User access to the standard models and records required by the configured POS.

This addon does not depend on `point_of_sale`, so it can be installed before or without the POS application. Odoo Online does not support third-party Python addons.

## Installation

1. Copy the `odeck_bridge` directory into an Odoo addons path.
2. Restart Odoo and update the Apps list.
3. Install **Odeck Bridge**.
4. Upgrade the module when deploying a newer release.

## POS integration

### Pricelist calculation

`product.pricelist.mobile_get_product_price` accepts a pricelist ID, product ID, quantity, and optional date. The addon checks read access and delegates rule selection and price calculation to the Odoo pricelist engine.

### Tax calculation

`account.tax.mobile_compute_all` accepts tax IDs, unit price, currency, quantity, product, customer, company, and refund context. The addon validates access and company scope before calling Odoo's standard tax engine. It returns the computed totals and JSON-safe tax details.

Both methods run as the authenticated user. They do not use `sudo()` to read business records and do not write business data. If a required method is missing or calculation fails, the client must not submit an estimated amount.

## Release branches

The `main` branch contains shared source. Odoo Apps release branches use the Odoo series as their branch name and the matching version prefix in the manifest, for example `17.0` with version `17.0.1.0.3`. The technical module name remains `odeck_bridge` across supported Odoo series.

## License and maintainer

Copyright © 2026 Linden Liu. Licensed under the GNU Lesser General Public License v3.0 (`LGPL-3`). See [LICENSE.md](LICENSE.md) for the license notice. Project website: <https://lindenliu.cn>.
