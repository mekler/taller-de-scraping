#!/usr/bin/python3
# -*- coding: utf-8 -*-
from scrape import Scrape
import json, math



class ComprasImss(Scrape):
    def __init__(self,headers=None):
        if headers == None:
            #valor de headers default
            headers = ['Origin: http://buscador.compras.imss.gob.mx','Accept-Encoding: gzip, deflate','Accept-Language: en-US,en;q=0.8,es;q=0.6','User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36','Content-Type: application/x-www-form-urlencoded','Accept: */*','Referer: http://buscador.compras.imss.gob.mx/wrap/index.html','X-Requested-With: WAJAF::Ajax - WebAbility(r) v5','Connection: keep-alive','DNT: 1']
        
        #inicializa el objeto que maneja las peticiones curl
        Scrape.__init__(self,headers)

        #inicializa el objeto mongo_client que se instancia en la clase Scrape
        #getattr hace una cosa como getattr('x','valor') ==> x.valor
        self.db = getattr(self.mongo_client, 'imss')
        self.compras = getattr(self.db, 'compras')
        self.raw = getattr(self.db, 'raw')

        #estos son los valores default de la página. se pueden modificar pero no lo haré para permanecer como bajo perfil
        self.numperpage = 20
        self.page=1
        self.url = 'http://buscador.compras.imss.gob.mx/index.php'
        self.datos_default = '&type=compras&message=X&filtered=1&descripcion=&proveedor=&numcompra=&delegacion=values%3D&fecha=min%3D%3Bmax%3D&procedimiento=values%3D&exact=false&numperpage={}&page={}&order=fecha%20desc'



    def buscaContratos(self,numperpage=20,page=1):
        print (self.datos_default.format(numperpage,page))

        #El true del final es para que descomprima el contenido
        self.pidePOST(self.url,self.datos_default.format(numperpage,page),True)

        #El objeto que regresa del curl es del tipo binary object. Se tiene que decodificar para que sea string.
        api_response = json.loads((self.response_string.decode(encoding='UTF-8')))


        #print (json.dumps(api_response, sort_keys=True, indent=4, separators=(',', ': ')))

        try:
            total_paginas = math.ceil(int(api_response['result']['quantity'])/float(api_response['result']['numperpage']))

            self.raw.insert(api_response)
            [self.compras.insert(elemento) for elemento in api_response['result']['data']]
            self.buscaContratos(numperpage,page+1)
        except Exception as e:
            print (e)
            self.refreshIP()
            self.buscaContratos(numperpage,page)

if __name__=='__main__':
    compras = ComprasImss()
    compras.buscaContratos()
    #compras.refreshIP()