# Bagron Net

Librería de red para el lenguaje Bagron. Incluye un cliente HTTP/HTTPS y un servidor estático local para pruebas y desarrollo.

- Versión de net: 1.0.0
- Versión mínima de Bagron: 1.1.4
- Estado: desarrollo activo

## ¿Qué incluye?

- `HttpClient`: cliente HTTP/HTTPS con soporte para GET y HEAD.
- `HttpServer`: servidor local estático.
- Validación de certificados TLS activa por defecto.
- Códigos de resultado del módulo como `NET_OK`, `NET_TIMEOUT` y `NET_NOT_FOUND`.

## Requisitos

- Bagron 1.1.4 o posterior, con las bibliotecas actuales de BagronLab instaladas.
- En Linux, `libcurl.so.4` debe estar disponible para HTTPS. Además, `gnulibrary.lib` debe incluir los nuevos enlaces `curl`, `open_cstr`, `read_chars`, `write_chars` y `OpenTcpHost`.

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

## ABI nativa compartida

`net` no contiene declaraciones `extern` propias. En sus puntos de entrada importa
`gnulibrary` para Linux o `windows` para Windows bajo el alias `Platform`.
Los sockets y la resolución DNS viven en las bibliotecas nativas de BagronLab,
incluidos sus helpers `OpenTcpHost` y `set_timeout`.

- `gnulibrary/modules/curl.bg`: API de libcurl y operaciones de libc requeridas para HTTPS.
- `gnulibrary/modules/{files,system,sockets}.bg`: syscalls y TCP para Linux.
- `windows/modules/winhttp.bg`: API nativa WinHTTP.
- `windows/modules/kernel32.bg`: `MultiByteToWideChar`.
- `windows/modules/sockets.bg`: conexión TCP, DNS y Winsock.

Los paquetes `*.lib` anteriores **no contienen estos cambios**: hay que
regenerarlos e instalarlos desde las fuentes actualizadas de BagronLab.
La compilación de la biblioteca `windows.lib` debe realizarse en un entorno Windows;
el empaquetador de Linux puede generar un paquete Windows sin símbolos exportados.

Prueba de humo validada en Linux x86_64 con Bagron 1.1.4:

```sh
bagron main.bg -o server-net
bagron client.bg -o client-net
# Ejecutar server-net en una terminal y client-net en otra.
# El cliente descarga main.bg desde 127.0.0.1:8000.
```

Windows y las transferencias HTTPS aún requieren pruebas de integración adicionales.

## Proyecto relacionado

- [Bagron](https://github.com/GrandKenzy/Bagron): lenguaje para el que está hecha esta librería.

## Pruebas

Consulta [tests/README.md](tests/README.md) para ver las pruebas de regresión y las comprobaciones del cliente y el servidor.
