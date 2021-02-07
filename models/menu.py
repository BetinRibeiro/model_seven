# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if auth.user:
    response.menu += [
        (T('Empresa'), False, URL('acs_empresa', 'index'), []),
        (T('Clientes'), False, URL('acs_cliente', 'index')),
        (T('Produtos'), False, URL('acs_produto', 'index')),
        (T('Vendas'), False, URL('acs_venda', 'index')),
    ]
