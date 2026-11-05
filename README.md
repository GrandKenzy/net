# Bagron Net

Librería de red para el lenguaje Bagron. Incluye un cliente HTTP/HTTPS y un servidor estático local para pruebas y desarrollo.

- Versión de net: 1.0.0
- Versión compatible de Bagron: 1.0.3
- Estado: desarrollo activo

## ¿Qué incluye?

- HttpClient: cliente HTTP/HTTPS con soporte para GET y HEAD
- HttpServer: servidor local estático
- Validación de certificados TLS activa por defecto
- Códigos de resultado del módulo como NET_OK, NET_TIMEOUT y NET_NOT_FOUND

## Requisitos

- Bagron compatible con la versión 1.0.3
- En Linux: libcurl.so.4 debe estar disponible para HTTPS

## Uso rápido

### Servidor local

```bg
import { HttpServer } from server

@unsafe
func main() int32:
    root: chain = "."
    host: chain = "127.0.0.1"
    server: HttpServer = HttpServer(
        $root[0], 1,
        $host[0], 9,
        8000, 10000, 8192
    )
    return server.run()
