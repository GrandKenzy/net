# Bagron Net

Librería de red para el lenguaje Bagron. Incluye un cliente HTTP/HTTPS y un servidor estático local para pruebas y desarrollo.

- Versión de net: 1.0.0
- Versión compatible de Bagron: 1.0.3
- Estado: desarrollo activo

## ¿Qué incluye?

- `HttpClient`: cliente HTTP/HTTPS con soporte para GET y HEAD.
- `HttpServer`: servidor local estático.
- Validación de certificados TLS activa por defecto.
- Códigos de resultado del módulo como `NET_OK`, `NET_TIMEOUT` y `NET_NOT_FOUND`.

## Requisitos

- Bagron compatible con la versión 1.0.3.
- En Linux, `libcurl.so.4` debe estar disponible para HTTPS.

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
```

### Cliente HTTP/HTTPS

```bg
import { HttpClient } from http

@unsafe
func main() int32:
    client: HttpClient = HttpClient(10000, 5, true)
    return client.get_to_file(
        "https://example.com/",
        "build/example.html"
    )
```

## Seguridad y limitaciones

- Este proyecto está diseñado principalmente para desarrollo local.
- No se recomienda exponer directorios modificables por usuarios no confiables.
- La validación TLS permanece activa por defecto.
- El servidor todavía no comprueba si un enlace simbólico o reparse point dentro de la raíz apunta fuera de ella. Utiliza únicamente directorios de confianza.

## Proyecto relacionado

- [Bagron](https://github.com/GrandKenzy/Bagron): lenguaje para el que está hecha esta librería.

## Pruebas

Consulta [tests/README.md](tests/README.md) para ver las pruebas de regresión y las comprobaciones del cliente y el servidor.
