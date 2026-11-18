# Odeck Bridge

[English](README.md) | 简体中文

Odeck Bridge 是一个可选的 Odoo 插件，为 POS 价格表与税额精算提供经过权限检查的接口。源码和安装说明见 [英文文档](README.md)。

仓库按 Odoo Apps 发行方式组织，请选择与目标 Odoo 系列匹配的分支（`17.0`、`18.0`、`19.0` 或 `20.0`）。此模块免费，Manifest 未设置 `price`。

插件不需要激活码。只有当 Odeck 移动客户端的 POS 流程需要 Odoo 服务端价格表或税额计算时才需安装。基础登录以及标准库存、销售、看板和 POS 浏览不依赖此插件。

维护者：Linden Liu · <https://lindenliu.cn>

## 多语言

Python 源码中的用户可见字符串以英文编写，并使用 Odoo 翻译函数标记。简体中文翻译位于 `i18n/zh_CN.po`；Odoo 会依据当前用户语言显示已安装的翻译。
