# -*- coding: utf-8 -*-
import datetime
# lista de recebimentos do representante vem do acs_venda lista_representante

@auth.requires_login()
def lista_registro_empresa():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    mes=request.now.month
    ano=request.now.year
    if len(request.args) < 2:
        redirect(URL(args=[mes,ano]))
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)
    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.registro_empresa.empresa==empresa.id)&(db.registro_empresa.data_ocorrencia>=primeira_data)&(db.registro_empresa.data_ocorrencia<ultima_data)).select(orderby=db.registro_empresa.data_ocorrencia)
    total = db((db.registro_empresa.empresa==empresa.id)&(db.registro_empresa.data_ocorrencia>=primeira_data)&(db.registro_empresa.data_ocorrencia<ultima_data)).count()
    return locals()


@auth.requires_login()
def cadastrar_registro_empresa():
    response.view = 'generic.html' # use a generic view
    request.function='Inserir Recebimento'
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    db.registro_empresa.empresa.default=empresa.id
    db.registro_empresa.empresa.writable=False
    db.registro_empresa.empresa.readable=False
    form = SQLFORM(db.registro_empresa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('lista_registro_empresa'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)


@auth.requires_login()
def alterar_registro_empresa():
    response.view = 'generic.html' # use a generic view
    request.function='Alterar Despesa'
    registro_empresa = db.registro_empresa(request.args[0])
    db.registro_empresa.id.writable=False
    db.registro_empresa.id.readable=False
    form = SQLFORM(db.registro_empresa, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('lista_registro_empresa'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def lista_recebimento_cliente():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    mes=request.now.month
    ano=request.now.year
    if len(request.args) < 2:
        redirect(URL(args=[mes,ano]))
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)
    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.registro_cliente.empresa==empresa.id)&(db.registro_cliente.data_ocorrencia>=primeira_data)&(db.registro_cliente.data_ocorrencia<ultima_data)).select(orderby=db.registro_cliente.data_ocorrencia)
    total = db((db.registro_cliente.empresa==empresa.id)&(db.registro_cliente.data_ocorrencia>=primeira_data)&(db.registro_cliente.data_ocorrencia<ultima_data)).count()
    return locals()
@auth.requires_login()
def lista_venda():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    venda = db.venda(request.args[0])    
    rows = db((db.registro_cliente.venda==venda.id)).select(orderby=db.registro_cliente.data_ocorrencia)
    total = db((db.registro_cliente.venda==venda.id)).count()
    return locals()

@auth.requires_login()
def cadastrar_registro_cliente():
    response.view = 'generic.html' # use a generic view
    request.function='Inserir Recebimento'
    venda = db.venda(request.args[0])
    cliente = db.pessoa(venda.cliente)
    db.registro_cliente.venda.default=venda.id
    db.registro_cliente.venda.writable=False
    db.registro_cliente.venda.readable=False
    db.registro_cliente.cliente.default=cliente.id
    db.registro_cliente.cliente.writable=False
    db.registro_cliente.cliente.readable=False
    db.registro_cliente.empresa.default=cliente.empresa
    db.registro_cliente.empresa.writable=False
    db.registro_cliente.empresa.readable=False
    form = SQLFORM(db.registro_cliente).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('lista_venda', args=venda.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)

@auth.requires_login()
def alterar_registro_cliente():
    response.view = 'generic.html' # use a generic view
    request.function='Alterar Recebimento'
    registro_cliente = db.registro_cliente(request.args[0])
    venda = db.venda(registro_cliente.venda)
    db.registro_cliente.id.writable=False
    db.registro_cliente.id.readable=False
    db.registro_cliente.tipo.writable=True
    form = SQLFORM(db.registro_cliente, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('lista_venda', args=venda.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
# lista de recebimentos do representante vem do acs_venda lista_representante
def lista_representante():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    representante = db.usuario_empresa(request.args[0])
    mes=request.now.month
    ano=request.now.year
    if len(request.args) < 3:
        redirect(URL(args=[representante.id,mes,ano]))
    mes=request.args(1, cast=int)
    ano=request.args(2, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)
    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.registro_representante.representante==representante.id)&(db.registro_representante.data_ocorrencia>=primeira_data)&(db.registro_representante.data_ocorrencia<ultima_data)).select(orderby=db.registro_representante.data_ocorrencia)
    total = db((db.registro_representante.representante==representante.id)&(db.registro_representante.data_ocorrencia>=primeira_data)&(db.registro_representante.data_ocorrencia<ultima_data)).count()
    return locals()
@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    request.function='Inserir Recebimento'
    representante = db.usuario_empresa(request.args[0])
    db.registro_representante.representante.default=representante.id
    db.registro_representante.representante.writable=False
    db.registro_representante.representante.readable=False
    db.registro_representante.empresa.default=representante.empresa
    db.registro_representante.empresa.writable=False
    db.registro_representante.empresa.readable=False
    form = SQLFORM(db.registro_representante).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('lista_representante', args=representante.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)


@auth.requires_login()
def alterar():
    response.view = 'generic.html' # use a generic view
    request.function='Alterar Recebimento'
    registro_representante = db.registro_representante(request.args[0])
    representante = db.usuario_empresa(registro_representante.representante)
    db.registro_representante.id.writable=False
    db.registro_representante.id.readable=False
    form = SQLFORM(db.registro_representante, request.args(0, cast=int), deletable=True)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('lista_representante', args=representante.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
