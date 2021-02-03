# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    paginacao = 35
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        redirect(URL(args=1))
    total = db(db.pessoa.empresa==empresa.id).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db(db.pessoa.empresa==empresa.id).select(
      limitby=limites,orderby=~db.pessoa.id
      )
    consul=(request.args(1))
    if (consul):
        registros = db((db.pessoa.empresa==empresa.id)&((db.pessoa.cpf.contains(consul))|(db.pessoa.razaosocial_nome.contains(consul)))).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario, consul=consul)
@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    request.function='Cadastrar novo Cliente'
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    db.pessoa.representante.default=usuario.id
    db.pessoa.representante.writable=False
    db.pessoa.representante.readable=False
    db.pessoa.empresa.default=usuario.empresa
    db.pessoa.empresa.writable=False
    db.pessoa.empresa.readable=False
    db.pessoa.tipo.notnull=True
    db.pessoa.cpf.notnull=True
    db.pessoa.org_espedidor_cpf.notnull=True
    db.pessoa.rg.notnull=True
    db.pessoa.org_espedidor_rg.notnull=True
    db.pessoa.cep.notnull=True
    db.pessoa.telefone.notnull=True
    db.pessoa.celular.notnull=True
    form = SQLFORM(db.pessoa).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    return  dict(form=form)
@auth.requires_login()
def alterar(): return locals()

@auth.requires_login()
def lista_representante():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    representante = db.usuario_empresa(request.args[0])
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
        redirect(URL(args=[representante.id,1]))
    total = db((db.pessoa.empresa==empresa.id)&(db.pessoa.representante==representante.id)).count()
    paginas = total/paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[representante.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.pessoa.empresa==empresa.id)&(db.pessoa.representante==representante.id)).select(
      limitby=limites,orderby=~db.pessoa.id
      )
    consul=(request.args(2))
    if (consul):
        registros = db(((db.pessoa.empresa==empresa.id)&((db.pessoa.cpf.contains(consul))|(db.pessoa.razaosocial_nome.contains(consul))))&(db.pessoa.representante==representante.id)).select(limitby=(0,paginacao))
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario, consul=consul, representante=representante)
