# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    return locals()

@auth.requires_login()
def lista_cliente():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    cliente = db.pessoa(request.args(0, cast=int))
    if usuario.tipo=="Representante":
        if cliente.representante!=usuario.id:
            redirect(URL('default','index'))
    paginacao = 35
    if len(request.args) <= 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=[cliente.id,1]))
    total = db(db.venda.cliente==cliente.id).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[cliente.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db(db.venda.cliente==cliente.id).select(
      limitby=limites,orderby=~db.venda.id
      )
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, cliente=cliente, usuario=usuario)

@auth.requires_login()
def alterar_cliente():
    response.view = 'generic.html' # use a generic view
    cliente = db.pessoa(request.args(0, cast=int))
    db.pessoa.id.writable=False
    db.pessoa.id.readable=False
    db.pessoa.representante.requires = IS_IN_DB(db((db.usuario_empresa.empresa == cliente.empresa)&(db.usuario_empresa.ativo==True)&(db.usuario_empresa.tipo=='Representante')), 'usuario_empresa.id', '%(nome)s')
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    if usuario.tipo=="Representante":
        if cliente.representante!=usuario.id:
            redirect(URL('default','index'))
        db.pessoa.representante.writable=False
        db.pessoa.representante.readable=False
    form = SQLFORM(db.pessoa, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Projeto atualizado'
        redirect(URL('lista_cliente',args=cliente.id))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    id =db.venda.insert(empresa=usuario.empresa, cliente=request.args(0, cast=int), representante=usuario.id)
    redirect(URL('acs_item_venda','lista_venda',args=id))
    return locals()

@auth.requires_login()
def alterar():
    return locals()

@auth.requires_login()
def lista_itens_venda():
    return locals()

@auth.requires_login()
def alterar_itens_venda():
    return locals()
