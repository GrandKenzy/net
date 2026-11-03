# Bagron Net

**Versión de net:** 1.0.0  
**Versión compatible de Bagron:** 1.0.3  
**Estado:** desarrollo activo

Biblioteca HTTP/HTTPS y servidor estático local para Bagron.

La API pública actual usa las clases `HttpClient` y `HttpServer`. Las antiguas
funciones globales `download()` y `serve()` ya no forman parte de esta
biblioteca.

## Servidor local

El servidor integrado sustituye a `python -m http.server` para servir archivos
durante las pruebas y el desarrollo:

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

`HttpServer` atiende conexiones secuenciales y acepta `GET` y `HEAD`. Devuelve
archivos con `Content-Length`, tipos MIME básicos e `index.html` para rutas de
directorio. Las rutas inexistentes devuelven `404` y los intentos de traversal,
como `..` o `%2e%2e`, devuelven `403`. No hay listado de directorios ni rutas
dinámicas. El binding admite `127.0.0.1`, `0.0.0.0`, `::1` y `::`.

La entrada `main.bg` de esta carpeta ya arranca este servidor en el puerto
`8000`. El proceso permanece bloqueado hasta que se detiene externamente.

Los resultados comunes están definidos en `result.bg`: `NET_OK`,
`NET_INVALID_ARGUMENT`, `NET_BACKEND`, `NET_RESOLVE`, `NET_CONNECTION`,
`NET_PROTOCOL`, `NET_STATUS`, `NET_FILE`, `NET_HEADER`, `NET_RECEIVE`,
`NET_REDIRECT`, `NET_TIMEOUT`, `NET_LIMIT`, `NET_METHOD`, `NET_FORBIDDEN` y
`NET_NOT_FOUND`.

## HTTPS

`HttpClient` selecciona el backend según el esquema de la URL:

- Windows: WinHTTP, que usa Schannel y el almacén de certificados del sistema.
- Linux: libcurl (`libcurl.so.4`), que usa la validación TLS y el almacén de certificados del sistema.

La validación de certificados permanece activa por defecto. Las conexiones con
certificados autofirmados, expirados o cuyo hostname no coincide fallan.

En Linux el enlazador debe encontrar `libcurl.so.4`. En Debian/Ubuntu suele
estar proporcionado por `libcurl4`; para compilar desde un entorno de desarrollo
puede ser necesario instalar también el paquete de desarrollo de libcurl.

## Uso

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

El cliente valida el esquema, aplica timeout de socket a HTTP, rechaza estados
HTTP no exitosos y entiende respuestas `Content-Length` y `Transfer-Encoding:
chunked`. Puede seguir redirecciones HTTP hasta `max_redirects`, y acepta
hosts IPv4 o IPv6 entre corchetes, por ejemplo `http://[::1]:8000/main.bg`.
Para una comprobación sin crear archivo, `HttpClient.head(url)` emite una
petición `HEAD` HTTP y devuelve `NET_OK` cuando la respuesta es `2xx`.
La compatibilidad de TLS permanece activa por defecto; Windows aplica el
timeout mediante WinHTTP y Linux delega el transporte HTTPS en libcurl.

## Ejemplos

- `main.bg`: servidor local estático.
- `client.bg`: cliente que descarga desde el servidor local.

## Seguridad y limitaciones

- El servidor estático está destinado inicialmente a desarrollo y pruebas.
- Sirve los archivos contenidos en la raíz configurada, pero **no comprueba
  actualmente si un enlace simbólico o reparse point dentro de esa raíz apunta
  fuera de ella**. Utiliza exclusivamente directorios de confianza y no
  expongas raíces modificables por usuarios no confiables.
- El cliente HTTP valida los esquemas completos, controla la longitud de las
  cabeceras y comprueba errores de recepción y escritura. Las redirecciones
  HTTP absolutas hacia HTTPS utilizan el backend TLS correspondiente.
- En Linux, HTTPS configura límites de tiempo de conexión y de transferencia
  en libcurl. El uso de `curl_easy_setopt` para opciones numéricas atraviesa
  una frontera ABI variádica y requiere validación de compilación y ejecución
  por arquitectura antes de declararse compatible con todas las plataformas.
- Se necesitan pruebas de integración adicionales para respuestas HTTP
  malformadas, conexiones interrumpidas y rutas con enlaces simbólicos.

## Pruebas

El archivo `tests/test_url.bg` incluye pruebas de regresión de esquemas URL
y retorna `0` al superar todos los casos. Consulta [tests/README.md](tests/README.md)
para las pruebas de cliente, servidor y transferencia.
