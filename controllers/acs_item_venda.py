# -*- coding: utf-8 -*-
@auth.requires_login()
def index(): return locals()
@auth.requires_login()
def cadastrar(): return locals()
@auth.requires_login()
def alterar(): return locals()