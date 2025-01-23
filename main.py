# -*- coding: utf-8 -*-

import os, io
import sys
import threading

try: # python 2
    reload(sys)
    sys.setdefaultencoding('utf8')
except:
    pass

import json
import socket

try: # python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer
    moduloHTTPServer = HTTPServer
    moduloHTTPRequest = BaseHTTPRequestHandler
    from socketserver import ThreadingMixIn
except: # python 2
    import BaseHTTPServer
    moduloHTTPServer = BaseHTTPServer.HTTPServer
    moduloHTTPRequest = BaseHTTPServer.BaseHTTPRequestHandler
    from SocketServer import ThreadingMixIn

from redirecciones import esRutaValida, respuestaGet, respuestaPut, respuestaPost, mi_ip

servidorAC = None
MODO_WEB = False
verb = False

archivosValidos = ['index.html','favicon.ico']

def launch_server(ip='localhost', port=8000, v=False):
    global verb
    verb = v
    MODO_WEB = ip != 'localhost'

    if (MODO_WEB):
        print('Launch WEB Server ' + ip + ":" + str(port))
    else:
        print('Launch LOCAL Server ' + ip + ":" + str(port))
    sys.stdout.flush()
    run(ip, port)

class HandlerAC(moduloHTTPRequest):
    def _set_response(self, n=200, headers={'Content-type':'text/html'}, cors=True):
        self.send_response(n)
        self.send_header('Cache-Control', 'no-cache')
        for h in headers:
            self.send_header(h, headers.get(h))
        if cors:
          self.cors_headers()
        self.end_headers()

    def cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.cors_headers()
        self.end_headers()

    def do_GET(self):
        if (self.path == "/"):
            self.archivoStatico('index.html')
        elif (len(self.path) > 1 and self.path[1:] in archivosValidos):
            self.archivoStatico(self.path[1:])
        elif (len(self.path) > 1 and esRutaValida(self.path[1:])):
            self.redirigir(respuestaGet(self.path[1:], self.headers))
        else:
            self.error("[GET] Ruta {} inválida".format(self.path))

    def do_PUT(self):
        if (len(self.path) > 1 and esRutaValida(self.path[1:])):
            self.redirigir(respuestaPut(self.path[1:], self.headers, self.rfile))
        else:
            self.error("[PUT] Ruta {} inválida".format(self.path))

    def do_POST(self):
        if (len(self.path) > 1 and esRutaValida(self.path[1:])):
            self.redirigir(respuestaPost(self.path[1:], self.headers, self.rfile))
        else:
            self.error("[POST] Ruta {} inválida".format(self.path))

    def error(self, msg):
        print(msg)
        self._set_response(404)

    def archivoStatico(self, ruta):
        if (os.path.isfile(ruta)):
            self._set_response(200, {'Content-type':tipo_archivo(ruta)})
            # f = io.open(ruta, mode='r', encoding='utf-8')
            f = io.open(ruta, mode='rb')
            self.wfile.write(f.read())
            f.close()
        else:
            self._set_response(404)
            print("Archivo {} no econtrado".format(self.path))

    def redirigir(self, dataRespuesta):
        self._set_response(dataRespuesta["n"], dataRespuesta["headers"], False)
        self.wfile.write(dataRespuesta["contenido"])

class ServerAC(ThreadingMixIn, moduloHTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """

def run(host, port):
    global servidorAC
    servidorAC = ServerAC((host, port), HandlerAC)
    try:
        servidorAC.serve_forever()
    except KeyboardInterrupt:
        pass
    close_server()
    print('Exit...\n')

def close_server():
    servidorAC.server_close()
    exit()

def tipo_archivo(filename):
    # if filename[-4:] == '.css':
    #     return 'text/css'
    # if filename[-5:] == '.json':
    #     return 'application/json'
    # if filename[-3:] == '.js':
    #     return 'application/javascript'
    if filename[-4:] == '.ico':
        return 'image/x-icon'
    # if filename[-4:] == '.svg':
    #     return 'image/svg+xml'
    return 'text/html'

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Server')
    parser.add_argument('-v', dest="v", default=False, type=bool, help='Modo verborrágico.')
    parser.add_argument('-p', dest="PORT", default=8000, type=int, help='Puerto')
    args = parser.parse_args()
    PORT = (int(os.environ['PORT']) if 'PORT' in os.environ else args.PORT)
    # launch_server('localhost', PORT, args.v)
    launch_server(mi_ip(), PORT, args.v)