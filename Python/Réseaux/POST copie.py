#!/usr/bin/env python3
"""micro dedicated HTTP server"""

import socket
import time 
import sys 

mimed={'mp4:'video/mp4', 'jpg':'image/jpeg', 'png':'image/png', 'ico':'image/ico',
       'html':'text/html'}

def getRawFileData(fname):
    return open(fname, 'r+b').read()

def getMimeType2(ext):
    print(ext)
    global mimed 
    if ext in mimed :
        return mimed[ext]
    else :
        return ''
    
def display_http(data):
    print(data.decode('ascii').replace('\r\n', '\n'), end='')


def http200head(ressource, options):
    http = "HTTP/1.1 200 OK\r\n"
    http += "Date: " + time.asctime(time.gmtime()) + " GMT\r\n"
    http += "Expires: " + time.asctime(time.gmtime(time.time() + 3600)) + " GMT\r\n"
    http += "Cache-Control: public, max-age=10, immutable\r\n"  # Reduced max-age for testing
    http += f"ETag: ipsav1\\r\n"
    idx_ext = ressource[1].rfind('.')
    mimetype = getMimeType2(ressource[1][idx_ext+1:])
    http += "Content-Type: " + dct.get(extension, "application/octet-stream") + "\r\n"
    http += "\r\n"
    if mimetype  == "text/html": 
        http += "charset=UTF-8\r\n"


def httpGet(commande,options,sock):
    import os
    if commande[1] == '/':
        commande[1] = '/index.html'
    ressource = commande[1]
    print('SRV : ressource : ./www' + ressource)
    if os.path.isfile('./www' + ressource):
        print('SRV: ressource foud')
        data = getRawFileData('./www + ressource)')
        head = http200head(ressource, options)
        sock.send(head+data)

    else :
        print("SRV : 404 Not found")
        sock.send(b'HTTP/1.1 404 Not Found\r\n\r\n<!DOCTYPE html><html><body><h1>404 not found</h1></body></html>\r\n')

def analyserequeqt2(request):
    sep = request.find('b\r\n\r\n')
    req = request[:sep].decode('ascii').split('\r\n')
    data = request[sep+4:]
    commande = req[0].split(' ')
    opt = req[1:]
    options={}
    for o in opt:
        l = o.split(':')
        options[l[0]]=l[1]
    return (commande,options,data)

served=0 # Belech 

def serve (data, comm_sock):
    global served
    commande,o,d = analyserequeqt2(data)
    print("\nCommand line:\n",commande)
    print("\nOptions: \n",o)
    print("\nData: \n",d)
    if commande[0] =='GET':
        httpGet(commande,o,comm_sock)
    elif commande[0] == 'POST' :
        print("command !:" , d.decode('ascii'))
        if True : # Served>=1
            r = 'HTTP/1.1 303 Not Modified\r\n'
            r += "Date: " + time.asctime(time.gmtime())+ " GMT\R\n"
            r += "Etag : ipsav1\r\n"
            r += "Exprires: "+ time.asctime(time.gmtime(time.time() +3600))+ "GMT\r\n"
            r += "Cache-Control : public, max-age=600, immutable\r\n"
            r += "Content-Type: text/html;"
            if getMimeType2(commande[1][commande[1].rfind('.')+1:]) == 'text/html':
                r +="charset=UTF-8\r\n"
            else :
                r +='\r\n'
            r+= '\r\n'
            print("response:\n", r.replace('\r\n','\n'))
            comm_sock.send(r.encode('ascii'))
        else :
            served+=1
            httpGet(commande,o,comm_sock)
    elif commande[0] == '':
        print("empty read")
    else:
        print("SRV ----- 405 Method Not Allowed ---------")
        print(data.decode('ascii'))
        print("----------------------")
        comm_sock.send(b'HTTP/1.1 405 Method Not allowed\r\n\r\n')

def main():
    
                                