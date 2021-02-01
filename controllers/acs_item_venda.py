# -*- coding: utf-8 -*-
@auth.requires_login()
def index(): return locals()
@auth.requires_login()
def cadastrar(): return locals()
@auth.requires_login()
def alterar(): return locals()

@auth.requires_login()
def lista_venda():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    venda = db.venda(request.args(0, cast=int))
    cliente = db.pessoa(db.pessoa.id==venda.cliente)
    ret=request.args(1)
    if ret:
        redirect(URL('acs_clientes','acessar', args=cliente.id))
    paginacao = 200
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=[venda.id,1]))
    total = db(db.item_venda.venda==venda.id).count()
    paginas = total/paginacao
    if (total%paginacao)or(paginas<1):
        paginas+=1
    if pagina > paginas:
        redirect(URL(args=[venda.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db(db.item_venda.venda==venda.id).select(
      limitby=limites,orderby=~db.item_venda.id
      )
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, venda=venda, cliente=cliente, usuario=usuario)

@auth.requires_login()
def buscar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    venda = db.venda(request.args(0, cast=int))
    cliente = db.pessoa(db.pessoa.id==venda.cliente)
    paginacao = 35
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=[venda.id,1]))
    total = db((db.produto.empresa==empresa.id)&(db.produto.ativo==True)).count()
    paginas = total/paginacao
    if (total%paginacao)or(paginas<1):
        paginas+=1
    if pagina > paginas:
        redirect(URL(args=[venda.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.produto.empresa==empresa.id)&(db.produto.ativo==True)).select(
      limitby=limites,orderby=~db.produto.id
      )
    consul=(request.args(2))
    if (consul):
        registros = db(((db.produto.empresa==empresa.id)&(db.produto.descricao.contains(consul)))&(db.produto.ativo==True)).select(limitby=(0,paginacao))
    rows_sub = db(db.item_venda.venda==venda.id).select()
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, venda=venda, cliente=cliente, rows_sub=rows_sub)

@auth.requires_login()
def escolher_item():
    response.view = 'generic.html' # use a generic view
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    produto = db.produto(request.args(0, cast=int))
    request.function=produto.descricao    
    venda = db.venda(request.args(1, cast=int))
    db.item_venda.empresa.default=usuario.empresa
    db.item_venda.produto.default=produto.id
    db.item_venda.venda.default=venda.id
    db.item_venda.representante.default=usuario.id
    form = SQLFORM(db.item_venda).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        item_venda = db.item_venda(form.vars.id)
        item_venda.custo_unitario=produto.custo_unitario
        item_venda.preco_unitario=produto.preco_unitario
        item_venda.update_record()
        redirect(URL('lista_venda', args=venda.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)
@auth.requires_login()
def excluir():
    response.view = 'generic.html' # use a generic view
    item_venda = db.item_venda(request.args(0, cast=int))
    venda = db.venda(item_venda.venda)
    db(db.item_venda.id==request.args(0, cast=int)).delete()
    redirect(URL('lista_venda', args=venda.id))
    return locals()
@auth.requires_login()
def fechar_pedido():
    venda = db.venda(request.args(0, cast=int))
    if venda.status=='Aberto':
        venda.status='Fechado'
    elif venda.status=='Fechado':
        venda.status='Aberto'
    venda.update_record()
    redirect(URL('lista_venda', args=venda.cliente))
    return locals()
