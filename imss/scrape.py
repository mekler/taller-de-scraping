#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pycurl, zlib
from io import BytesIO
from bs4 import BeautifulSoup

import subprocess

#codificación a utf-8
import sys
import time 
#reload(sys)
#sys.setdefaultencoding('UTF8')

import pymongo
from pymongo import MongoClient

import logging, re

class Scrape:
    contador=0
    def __init__(self,headers):
        super(Scrape,self).__init__()
        self.headers = headers
        self.mongo_client = MongoClient('localhost', 27017)
        self.response_string = None
        self.url = None
        self.ip_actual = '0.0.00.'
        self.ip_anterior = None
        self.ip_actual = self.refreshIP()
        #logging.basicConfig(level=logging.DEBUG)
        #self.log = logging.getLogger('test')

    def regresaOpcionesDeSelect(self,url,lista,demo=False):
        self.pideURL(url)
        if self.response_string is not None:
            soup = BeautifulSoup(self.response_string, 'lxml')
            if demo:
                print (soup.prettify())
            for option in soup.find_all('option'):
                if option['value']!=self.valor_default:
                    lista.append(option['value'])

    def refreshIP(self):
        resp = False
        print ("Refreshing IP...")
        try:
            process = subprocess.Popen(['sudo','service','tor', 'restart'], shell=False, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            #process.stdin.write('hakunami\n')
            #process.stdin.flush()
            stdout, stderr = process.communicate()

            print ('Tor restart info: ', stdout)

            ipchecker = subprocess.Popen(['/usr/bin/GET', 'http://clientn.free-hideip.com/map/whatismyip.php', '-p', 'http://127.0.0.1:8118'],
                                            shell=False, stdout=subprocess.PIPE)
            stdout, stderr = ipchecker.communicate()
            IP = re.search('\d+\.\d+\.\d+\.\d+',stdout.decode(encoding='UTF-8'))
            if IP:
                if IP==self.ip_anterior:
                    self.refreshIP()
                print ('Current using IP is: ', IP.group(0))
                resp = True
                self.ip_anterior = self.ip_actual
                self.ip_actual = IP
            Scrape.contador = 0

        except Exception as e:
            print ("Failed to Refresh IP.", e)

        return resp

    def pideURL(self,url,compressed = False, cookie=False, contador_curl = 0):
        time.sleep(3)
        Scrape.contador+=1
        print ("\n"+url)
        print ("\n\t.l."+str(Scrape.contador))
        c = pycurl.Curl()
        if cookie:
            c.setopt(pycurl.COOKIEJAR, 'cookie.txt')
            c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
        c.setopt(pycurl.URL, url)       
        c.setopt(pycurl.CONNECTTIMEOUT, 15) 
        c.setopt(pycurl.TIMEOUT, 25) 
        c.setopt(pycurl.HTTPHEADER, self.headers)

        c.setopt( pycurl.PROXY, '127.0.0.1' )
        c.setopt( pycurl.PROXYPORT, 9050 )
        c.setopt( pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME )
        
        b = BytesIO()
        BytesIO
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        self.url = url
        try:
            c.perform()
            self.response_string = b.getvalue()
            #print (self.response_string)
            b.close()
        except Exception as e:
            #self.log ('Razon:',e)

            self.response_string = None
            if contador_curl<=10:
                time.sleep(5)
                self.pideURL(url,contador_curl+1)
            else:
                print ('Error: ',url)
                print ('Error log: ',e)

    def pidePOST(self,url,data,compressed = False,cookie=False, contador_curl = 0, debug=False):
        time.sleep(3)
        Scrape.contador+=1
        print ("\n"+url)
        print ("\n\t.l."+str(Scrape.contador))
        c = pycurl.Curl()
        if cookie:
            c.setopt(pycurl.COOKIEJAR, 'cookie.txt')
            c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.CONNECTTIMEOUT, 15)
        c.setopt(pycurl.TIMEOUT, 25)
        c.setopt(pycurl.HTTPHEADER, self.headers)

        if compressed:
            c.setopt(pycurl.ENCODING, 'gzip,deflate')

        c.setopt(c.POSTFIELDS, data)
        
        if debug:
            c.setopt(c.VERBOSE, True)

        c.setopt( pycurl.PROXY, '127.0.0.1' )
        c.setopt( pycurl.PROXYPORT, 9050 )
        c.setopt( pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5_HOSTNAME )
        
        b = BytesIO()
        BytesIO
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        self.url = url
        try:
            c.perform()
            self.response_string = b.getvalue()
            #print (self.response_string)
            b.close()
        except Exception as e:
            #print ('Razon:',e)
            self.response_string = None