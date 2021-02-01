# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    paginacao = 35
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'}))
    if pagina <= 0:
        redirect(URL(args=1))
    #total = db(db.produto.empresa==empresa.id).delete()
    total = db(db.produto.empresa==empresa.id).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db(db.produto.empresa==empresa.id).select(
      limitby=limites,orderby=~db.produto.id
      )
    consul=(request.args(1))
    if (consul):
        registros = db((db.produto.empresa==empresa.id)&((db.produto.descricao.contains(consul)))).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario)
@auth.requires_login()
def lista_produto():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    fornecedor = db.fornecedor(request.args(0, cast=int))
    paginacao = 15
    if len(request.args) <= 1:
        redirect(URL(args=[fornecedor.id,1]))
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=[fornecedor.id,1]))
    total = db(db.produto.fornecedor==fornecedor.id).count()
    total_empresa = db(db.produto.empresa==fornecedor.empresa).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[fornecedor.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db(db.produto.fornecedor==fornecedor.id).select(
      limitby=limites,orderby=~db.produto.id
      )
    consul=(request.args(2))
    if (consul):
        registros = db((db.produto.fornecedor==fornecedor.id)&(db.produto.descricao.contains(consul))).select(limitby=(0,paginacao))
        paginas=1
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, fornecedor=fornecedor, usuario=usuario, total_empresa=total_empresa,consul=consul)
@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    db.produto.fornecedor.default=request.args(0, cast=int)
    db.produto.fornecedor.writable=False
    db.produto.fornecedor.readable=False
    db.produto.empresa.default=usuario.empresa
    form = SQLFORM(db.produto).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('lista_produto',args=request.args(0, cast=int)))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)
@auth.requires_login()
def alterar():
    response.view = 'generic.html' # use a generic view
    produto = db.produto(request.args(0, cast=int))
    db.produto.id.writable=False
    db.produto.id.readable=False
    db.produto.fornecedor.writable=False
    db.produto.fornecedor.readable=False
    db.produto.custo_unitario.writable=True
    db.produto.custo_unitario.readable=True
    db.produto.ativo.writable=True
    db.produto.ativo.readable=True
    form = SQLFORM(db.produto, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        session.flash = 'Dados atualizados'
        redirect(URL('lista_produto',args=produto.fornecedor))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)

@auth.requires_login()
def lista_itens_venda(): return locals()
@auth.requires_login()
def alterar_itens_venda(): return locals()
