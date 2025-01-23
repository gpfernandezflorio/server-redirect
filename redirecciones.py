import requests
import socket

# Diccionario que asocia rutas a puertos
RUTAS_VALIDAS = {
  "aele":8005 # TODO: ir al buscarlo al archivo .env de aele
}

# Puertos del robotutor
Puerto_inicial_robotutor = 8050 # TODO: ir al buscarlo al archivo info.json del robotutor
for i in range(Puerto_inicial_robotutor, Puerto_inicial_robotutor+11):
  RUTAS_VALIDAS[f"robotutor_{i}"] = i

def esRutaValida(url):
  urlPrincipal = url.split("/")[0]
  print(urlPrincipal)
  return urlPrincipal in RUTAS_VALIDAS

def respuestaGet(url, headers):
  urlPrincipal = url
  dataAdicional = ""
  iBarra = url.find("/")
  if iBarra > 0:
    urlPrincipal = url[0:iBarra]
    dataAdicional = url[iBarra:]
  puerto = RUTAS_VALIDAS[urlPrincipal]
  resultado = requests.get('http://'+str(mi_ip())+':'+str(puerto)+dataAdicional, headers=headers)

  return {
    "n":resultado.status_code,
    "headers":resultado.headers,
    "contenido":resultado.content
  }

def respuestaPut(url, headers, data):
  urlPrincipal = url
  dataAdicional = ""
  iBarra = url.find("/")
  if iBarra > 0:
    urlPrincipal = url[0:iBarra]
    dataAdicional = url[iBarra:]
  puerto = RUTAS_VALIDAS[urlPrincipal](dataAdicional)
  resultado = requests.put('http://'+str(mi_ip())+':'+str(puerto)+dataAdicional, headers=headers, data=data)

  return {
    "n":resultado.status_code,
    "headers":resultado.headers,
    "contenido":resultado.content
  }

def respuestaPost(url, headers, data):
  urlPrincipal = url
  dataAdicional = ""
  iBarra = url.find("/")
  if iBarra > 0:
    urlPrincipal = url[0:iBarra]
    dataAdicional = url[iBarra:]
  puerto = RUTAS_VALIDAS[urlPrincipal](dataAdicional)
  resultado = requests.post('http://'+str(mi_ip())+':'+str(puerto)+dataAdicional, headers=headers, data=data)

  return {
    "n":resultado.status_code,
    "headers":resultado.headers,
    "contenido":resultado.content
  }

def mi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
    return s.getsockname()[0]