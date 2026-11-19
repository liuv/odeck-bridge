# Odeck Bridge

![Odeck Mobile for Odoo — product, performance, and order screens](assets/marketing/odeck-mobile-hero.png)

Odeck Bridge is a free, optional Odoo addon that lets the Odeck mobile POS client use Odoo's standard pricelist and tax engines. Choose the branch matching your Odoo version, then copy the `odeck_bridge` folder into your addons path.

[Installation and technical documentation](odeck_bridge/README.md) · [简体中文](odeck_bridge/README.zh_CN.md) · [License](odeck_bridge/LICENSE.md)

## Odeck Mobile

Odeck Mobile connects to your own Odoo server and provides a mobile view for products, sales orders, inventory, sales performance, and POS workflows. Odeck Bridge is only required for server-side POS pricelist and tax calculations; ordinary login, browsing, and order viewing use Odoo's standard APIs.

The banner above is a generated product illustration. The screens below use app simulator captures presented in iPhone frames. The sales performance screen uses illustrative demo figures, not live customer data.

| Product catalog | Sales performance |
| --- | --- |
| ![Product catalog in an iPhone frame](assets/marketing/products-iphone.png) | ![Sales performance with illustrative demo figures in an iPhone frame](assets/marketing/performance-iphone.png) |

| Sales orders | Navigation menu |
| --- | --- |
| ![Sales orders in an iPhone frame](assets/marketing/sales-orders-iphone.png) | ![Expanded navigation menu in an iPhone frame](assets/marketing/navigation-menu-iphone.png) |

## Android APK downloads

When a signed Android release is available, download the APK from [GitHub Releases](https://github.com/liuv/odeck-bridge/releases). The APK is distributed as a release asset rather than inside the Odoo addon. Check the release notes for the app version, supported Odoo versions, and SHA-256 checksum.

Android updates must keep the same signing identity as the installed app. Development/debug builds are not suitable as update packages. Odeck Bridge does not download or install the APK; users install the mobile client separately.

## Branches

- `17.0` — Odoo 17
- `18.0` — Odoo 18
- `19.0` — Odoo 19
- `20.0` — Odoo 20

See the [addon documentation](odeck_bridge/README.md) for requirements, installation, and POS endpoint details.
