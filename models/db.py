# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

db.define_table('empresa',
                Field('proprietario','reference auth_user', label='Proprietario', writable=False, readable=False, notnull=True, default=1),
                Field('razaosocial', 'string', label='Razão Social',requires = IS_UPPER()),
                Field('nomefantasia', 'string', label='Nome Fantasia',requires = IS_UPPER()),
                Field('cnpj', 'string', label='CNPJ',default="00.000.000/0001-00",requires = IS_UPPER()),
                Field('inscricaoestarual', 'string',default="00000", label='Insc. Est',requires = IS_UPPER()),
                Field('inscricaomunicipal', 'string',default="00000", label='Insc. Mun',requires = IS_UPPER()),
                Field('crt', 'string', label='CRT',default="00000",requires = IS_UPPER()),
                #endereco
                Field('cep', 'string', label='CEP',default="60000-000",requires = IS_UPPER()),
                Field('lougradouro', 'string', label='Lougradouro',default="Rua",requires = IS_UPPER()),
                Field('numero', 'string', label='Numero',default="0",requires = IS_UPPER()),
                Field('bairro', 'string', label='Bairro',default="Centro",requires = IS_UPPER()),
                Field('uf', 'string', label='UF',default="CE",requires = IS_UPPER()),
                Field('cidade', 'string', label='Cidade', default='Juazeiro do Norte',requires = IS_UPPER()),
                Field('complemento', 'string', label='Complemento',default="Sem Complemento",requires = IS_UPPER()),
                #contato
                Field('email', 'string', label='Email',default="sem@email.com",requires = IS_UPPER()),
                Field('telefone', 'string', label='Telefone',default="(88)3500-0000",requires = IS_UPPER()),
                Field('celular', 'string', label='Celular',default="(88)99000-0000",requires = IS_UPPER()),
                #quantidade dependendo do pacote que contrate
                Field('limite_clientes', 'integer', label='L Clientes', writable=False, readable=False, default=1000),
                Field('limite_logins', 'integer', label='L Logins', writable=False, readable=False, default=4),
                Field('limite_produtos', 'integer', label='L Produtos', writable=False, readable=False, default=200),
                Field('limite_fornecedores', 'integer', label='L Fornecedores', writable=False, readable=False, default=200),
                Field('limite_vendas', 'integer', label='L Vendas', writable=False, readable=False, default=2000),
                Field('data_bloqueio', 'date', label="Data Bloqueio", writable=False, readable=False, default=request.now, requires = IS_DATE(format=('%d-%m-%Y')), notnull=True),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                auth.signature,
                format='%(nomefantasia)s')

db.define_table('usuario_empresa',
                Field('usuario','reference auth_user', writable=False, readable=False, label='Usuario'),
                Field('empresa','reference empresa', writable=False, readable=False, label='empresa'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('tipo', 'string', label='tipo',default='Representante'),
                Field('comissao', 'double', label='%Comissão', writable=True, readable=True, notnull=True, default=10),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                format='%(nome)s')

db.define_table('pessoa',
                Field('empresa','reference empresa', label='empresa', writable=False, readable=False),
                Field('representante','reference usuario_empresa', writable=True, readable=True, label='Representante'),
                Field('tipo', 'string', label='Tipo', writable=False, readable=False, default='Física',requires = IS_UPPER()),
                Field('razaosocial_nome', 'string', label='RS/NC',notnull=True ,requires=[IS_UPPER(),IS_LENGTH(minsize=12, error_message='Nome muito pequeno')]),
                Field('sexo', 'string', label='Sexo', default='M',notnull=True, writable=False, readable=False ,requires = IS_UPPER()),
                Field('estado_civil', 'string', label='Est. Civil',notnull=True , writable=False, readable=False, default='Solteiro(a)',requires = IS_UPPER()),
                Field('apelido_nome_fantasia', 'string', label='AP/NF', writable=False, readable=False,requires = IS_UPPER()),
                Field('cpf', 'string', label='CPF/CNPJ',notnull=True ,requires = IS_UPPER()),
                Field('org_espedidor_cpf', 'string', default='SSP', writable=False, readable=False,notnull=True , label='org esp.',requires = IS_UPPER()),
                Field('rg', 'string', label='RG',notnull=True ,requires = IS_UPPER()),
                Field('org_espedidor_rg', 'string', default='SSP', writable=False, readable=False,notnull=True , label='org esp.',requires = IS_UPPER()),
                Field('cep', 'string', label='CEP', default='63050-000',requires = IS_UPPER()),
                Field('lougradouro', 'string', label='Lougradouro',requires = IS_UPPER()),
                Field('numero', 'string', label='Numero',requires = IS_UPPER()),
                Field('bairro', 'string', default='Centro', label='Bairro',requires = IS_UPPER()),
                Field('uf', 'string', label='UF', default='CE',requires = IS_UPPER()),
                Field('cidade', 'string', label='Cidade', default='Juazeiro do Norte',requires = IS_UPPER()),
                Field('complemento', 'string', label='Complemento',requires = IS_UPPER()),
                Field('email', 'string', label='Email', default='sem@email.com',requires = IS_EMAIL(error_message='Email Invalido!')),
                Field('telefone', 'string', label='Telefone', default='(88)3555-5555',requires = IS_UPPER()),
                Field('celular', 'string',notnull=True , default='(88)98888-8888', label='Celular',requires = IS_UPPER()),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                auth.signature,
                format='%(razaosocial_nome)s')

db.define_table('fornecedor',
                Field('empresa','reference empresa', writable=False, readable=False, label='empresa'),
                Field('nome', 'string', label='Nome',requires = IS_UPPER()),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('telefone', 'string', label='Telefone',default="(88)3500-0000",requires = IS_UPPER()),
                Field('celular', 'string', label='Celular',default="(88)99000-0000",requires = IS_UPPER()),
                Field('total_compra', 'double', label='Total Compras', writable=False, readable=False, notnull=True, default=0),
                Field('total_pago', 'double', label='Total Pago', writable=False, readable=False, notnull=True, default=0),
                Field('total_devolvido', 'double', label='Total Devolvido', writable=False, readable=False, notnull=True, default=0),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                auth.signature,
                format='%(nome)s')

db.define_table('produto',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('fornecedor','reference fornecedor', writable=True, readable=True, label='Fornecedor'),
                Field('descricao', 'string', label='Descrição',requires = IS_UPPER()),
                Field('quant_estoque', 'integer', label='Q Estoque', writable=False, readable=False, default=0),
                Field('custo_unitario', 'double', label='Custo Unitario', writable=True, readable=True, notnull=True, default=0),
                Field('preco_unitario', 'double', label='Preço Unitario', writable=True, readable=True, notnull=True, default=0),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                auth.signature,
                format='%(descricao)s')
