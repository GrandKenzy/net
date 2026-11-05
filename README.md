# Bagron Net

Librería de red para el lenguaje Bagron. Proporciona un cliente HTTP/HTTPS y un servidor estático local para desarrollo y pruebas.

- Versión de net: 1.0.0
- Versión compatible de Bagron: 1.0.3
- Estado: desarrollo activo

## ¿Qué incluye?

- `HttpClient`: cliente HTTP/HTTPS con soporte para GET/HEAD, redirecciones, validación de TLS y manejo de cabeceras.
- `HttpServer`: servidor local estático para servir contenido desde un directorio raíz.
- Soporte para `http://` y `https://` con validación de certificados activa por defecto.
- Manejo de errores con códigos de resultado del módulo (`NET_OK`, `NET_TIMEOUT`, `NET_NOT_FOUND`, etc.).

## Requisitos

- Compilador o runtime de Bagron compatible con la versión 1.0.3.
- En Linux, `libcurl.so.4` debe estar disponible para HTTPS.
- En Debian/Ubuntu, normalmente se resuelve instalando `libcurl4` y, si es necesario, el paquete de desarrollo `libcurl4-openssl-dev`.

## Instalación

Este repositorio se usa como librería del lenguaje Bagron, importando los módulos que expone el proyecto.

```bg
import { HttpClient } from http
import { HttpServer } from server
```

## Uso rápido

### Servidor estático local

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

`HttpServer` sirve archivos locales desde una raíz configurada, ofrece `GET` y `HEAD`, devuelve `Content-Length`, emplea tipos MIME básicos y gestionará `index.html` en rutas de directorio.

- Ruta inexistente: `404`
- Intento de traversal (`..`, `%2e%2e`): `403`
- No ofrece listado de directorios ni rutas dinámicas
- Soporta `127.0.0.1`, `0.0.0.0`, `::1` y `::`

El archivo `main.bg` del repositorio arranca el servidor en el puerto `8000`.

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

El cliente:

- valida el esquema de la URL;
- aplica timeout de conexión y transferencia;
- rechaza estados HTTP no exitosos;
- entiende `Content-Length` y `Transfer-Encoding: chunked`;
- sigue redirecciones HTTP hasta un máximo configurable;
- acepta hosts IPv4 e IPv6 con formato estándar, como `http://[::1]:8000/main.bg`.

También dispone de `HttpClient.head(url)`, útil para comprobar si un recurso responde correctamente sin guardar el archivo en disco.

## HTTPS y TLS

`HttpClient` selecciona el backend según el esquema de la URL:

- Windows: WinHTTP, con Schannel y el almacén de certificados del sistema.
- Linux: libcurl (`libcurl.so.4`), con validación TLS y almacenamiento del sistema.

La validación de certificados permanece activa por defecto. Certificados autofirmados, caducados o con hostname incorrecto fallarán.

## Seguridad y limitaciones

Este proyecto está pensado principalmente para desarrollo y pruebas locales.

- El servidor estático sirve únicamente el contenido de la raíz configurada.
- Se debe usar únicamente con directorios de confianza.
- No se recomienda exponer directorios modificables por usuarios no confiables.
- La validación de rutas y el control de acceso se deben evaluar con cuidado cuando se emplea en entornos no seguros.
- En Linux, la capa HTTPS depende de libcurl y debe probarse en cada arquitectura objetivo antes de asumir compatibilidad total.

## Estructura del repositorio

- `main.bg`: ejemplo de servidor local.
- `client.bg`: ejemplo de cliente HTTP.
- `modules/`: módulos del proyecto.
- `tests/`: pruebas de regresión y validación.
- `README.md`: documentación principal.
- `CHANGELOG.md`: historial de cambios.

## Pruebas

El repositorio incluye pruebas de regresión bajo `tests/`.

Consulta [tests/README.md](tests/README.md) para ver:

- pruebas de URL y esquemas;
- validaciones de cliente y servidor;
- casos de robustez y redirecciones;
- comprobaciones específicas de HTTP/HTTPS.

## Proyecto relacionado

- [Bagron](https://github.com/GrandKenzy/Bagron): lenguaje base del que esta librería depende.

## Estado actual

La API pública actual usa las clases `HttpClient` y `HttpServer`. Las funciones globales antiguas `download()` y `serve()` ya no forman parte de esta biblioteca.

Si quieres colaborar, prueba el cliente y el servidor con archivos locales, revisa los casos de regresión y comparte cualquier error o mejora que encuentres.
