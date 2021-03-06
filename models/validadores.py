# -*- coding: utf-8 -*-
#validadores da empresa
db.empresa.celular.requires = IS_MATCH('^\(?\d{2}\)?\d{5}\-?\d{4}$', error_message='Formato (00)0000-0000'),
db.empresa.uf.requires=IS_IN_SET(['RO','AC','AM','RR','PA','AP','TO','MA','PI','CE','RN','PB','PE','AL','SE','BA','MG','ES','RJ','SP','PR','SC','RS','MS','MT','GO','DF'])
db.empresa.cep.requires = IS_MATCH('^\d{5}\-?\d{3}$', error_message='Formato 63000-000'),
db.empresa.celular.requires = IS_MATCH('^\(?\d{2}\)?\d{5}\-?\d{4}$', error_message='Formato (00)00000-0000'),
db.empresa.telefone.requires = IS_MATCH('^\(?\d{2}\)?\d{4}\-?\d{4}$', error_message='Formato (00)0000-0000'),

#validadores dos clientes
db.pessoa.telefone.requires = IS_MATCH('^\(?\d{2}\)?\d{4}\-?\d{4}$', error_message='Formato (00)0000-0000'),
db.pessoa.celular.requires = IS_MATCH('^\(?\d{2}\)?\d{5}\-?\d{4}$', error_message='Formato (00)0000-0000'),
db.pessoa.cpf.requires  = IS_MATCH('^\d{3}\.?\d{3}\.?\d{3}\-?\d{2}|\d{2}\.?\d{3}\.?\d{3}\/?\d{4}\-?\d{2}$', error_message='cpf - 000.000.000-00 ou cnpj 00.000.000/0001-00'),
db.pessoa.tipo.requires = IS_IN_SET(['Física','Jurídica'])
db.pessoa.uf.requires=IS_IN_SET(['RO','AC','AM','RR','PA','AP','TO','MA','PI','CE','RN','PB','PE','AL','SE','BA','MG','ES','RJ','SP','PR','SC','RS','MS','MT','GO','DF'])
db.pessoa.sexo.requires = IS_IN_SET(['M','F'])
db.pessoa.estado_civil.requires = IS_IN_SET(['Solteiro(a)','Casado(a)'])

#usuario da empresa
db.usuario_empresa.tipo.requires = IS_IN_SET(['Representante','Administrador','Proprietário'])

#fornecedor

db.fornecedor.celular.requires = IS_MATCH('^\(?\d{2}\)?\d{5}\-?\d{4}$', error_message='Formato (00)00000-0000'),
db.fornecedor.telefone.requires = IS_MATCH('^\(?\d{2}\)?\d{4}\-?\d{4}$', error_message='Formato (00)0000-0000'),
#validador da venda
db.venda.status.requires = IS_IN_SET(['Aberto','Fechado','Conferido','Entregue','Devolvido','Quitado'])

#registro de cheques dos clientes
db.registro_cliente.tipo.requires = IS_IN_SET(['Pagamento','Cheque Voltou'])
