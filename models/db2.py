# -*- coding: utf-8 -*-

db.define_table('registro_empresa',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('data_ocorrencia', 'date', label="Data", writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('descricao', 'string', label='Descrição', writable=True, readable=True,requires = IS_UPPER()),
                Field('valor', 'double', label='Valor', writable=True, readable=True, notnull=True, default=0),
                Field('tipo', 'string', default='Despesa', writable=False, readable=False, label='Tipo'),
                Field('conferida', 'boolean', writable=False, readable=False, default=False),
                auth.signature,
                format='%(codigo)s')

db.define_table('registro_representante',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('representante','reference usuario_empresa', writable=False, readable=False, label='Representante'),
                Field('data_ocorrencia', 'date', label="Data", writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('descricao', 'string', label='Descrição', writable=True, readable=True,requires = IS_UPPER()),
                Field('valor', 'double', label='Valor', writable=True, readable=True, notnull=True, default=0),
                Field('tipo', 'string', default='Vale', writable=False, readable=False, label='Tipo'),
                Field('conferida', 'boolean', writable=False, readable=False, default=False),
                auth.signature,
                format='%(descricao)s')

db.define_table('registro_cliente',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('cliente','reference pessoa', writable=False, readable=False, label='Cliente'),
                Field('venda','reference venda', writable=False, readable=False, label='Venda'),
                Field('data_ocorrencia', 'date', label="Data", writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('descricao', 'string', label='Descrição', writable=True, readable=True,requires = IS_UPPER()),
                Field('valor', 'double', label='Valor', writable=True, readable=True, notnull=True, default=0),
                Field('tipo', 'string', default='Pagamento', writable=False, readable=False, label='Tipo'),
                Field('conferida', 'boolean', writable=False, readable=False, default=False),
                auth.signature,
                format='%(descricao)s')
