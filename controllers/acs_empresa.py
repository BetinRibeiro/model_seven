# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario_empresa = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario_empresa.empresa)
    if not usuario_empresa:
        redirect(URL('acs_empresa','cadastrar'))
        qproj_abertos=db((db.projeto.empresa==usuario_empresa.empresa)&(db.projeto.ativo==True)).count()
        if (qproj_abertos)>0:
            aberto=True
    return locals()

@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    a=db.empresa.insert(razaosocial=auth.user.first_name,nomefantasia=auth.user.first_name)
    db.usuario_empresa.insert(empresa=a,usuario=auth.user.id, nome=auth.user.first_name, tipo="Proprietário")
    redirect(URL('index'))
    return locals()

@auth.requires_login()
def alterar(): return locals()
