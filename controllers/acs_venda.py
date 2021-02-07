# -*- coding: utf-8 -*-
import datetime

@auth.requires_login()
def lista_recebimento():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    mes=request.now.month
    ano=request.now.year
    if len(request.args) == 0:
        redirect(URL(args=[mes,ano]))
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)
    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.venda.empresa==empresa.id)&(db.venda.status=="Entregue")&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).select(orderby=db.venda.data_venda)
    total = db((db.venda.empresa==empresa.id)&(db.venda.status=="Entregue")&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).count()
    return locals()

@auth.requires_login()
def lista_vendas_representante():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    mes=request.now.month
    ano=request.now.year
    if len(request.args) == 0:
        redirect(URL(args=[mes,ano]))
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)
    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.venda.representante==usuario.id)&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).select(orderby=db.venda.data_venda)
    total = db((db.venda.representante==usuario.id)&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).count()
    return locals()
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if usuario.tipo=="Representante":
        redirect(URL('acs_venda','lista_vendas_representante'))
    empresa = db.empresa(usuario.empresa)
    mes=request.now.month
    ano=request.now.year
    if len(request.args) == 0:
        redirect(URL(args=[mes,ano]))
    mes=request.args(0, cast=int)
    ano=request.args(1, cast=int)
    primeira_data=datetime.date(ano, mes, 1)
    ultima_data=datetime.date(ano, mes, 1)
    if (mes==12):
        ultima_data=datetime.date(ano+1, 1, 1)
    else:
        ultima_data=datetime.date(ano, mes+1, 1)
    rows = db((db.venda.empresa==empresa.id)&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).select(orderby=db.venda.data_venda)
    total = db((db.venda.empresa==empresa.id)&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).count()
    return locals()

@auth.requires_login()
def lista_cliente():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('default','index'))
    empresa = db.empresa(usuario.empresa)
    cliente = db.pessoa(request.args[0])
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
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa,cliente=cliente, usuario=usuario)

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


@auth.requires_login()
def atualiza_status():
    response.view = 'generic.html' # use a generic view
    venda = db.venda(request.args(0, cast=int))
    status = request.args(1, cast=str)
    venda.status = status
    venda.update_record()
    rows = db(db.item_venda.venda==venda.id).select()
    for row in rows:
        row.status=venda.status
        row.update_record()
    redirect(URL('acs_item_venda','lista_status',args=venda.id))
    return locals()

@auth.requires_login()
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
    rows = db((db.venda.representante==representante.id)&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).select(orderby=db.venda.data_venda)
    total = db((db.venda.representante==representante.id)&(db.venda.data_venda>=primeira_data)&(db.venda.data_venda<ultima_data)).count()
    quant_vales = db((db.registro_representante.representante==representante.id)&(db.registro_representante.data_ocorrencia>=primeira_data)&(db.registro_representante.data_ocorrencia<ultima_data)).count()
    total_vales = 0
    if quant_vales>0:
        sum = db.registro_representante.valor.sum()
        total_vales = db((db.registro_representante.representante==representante.id)&(db.registro_representante.data_ocorrencia>=primeira_data)&(db.registro_representante.data_ocorrencia<ultima_data)).select(sum).first()[sum]
        
    return locals()
