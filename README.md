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
- En Linux x86_64, el servidor abre rutas mediante `openat2` con `RESOLVE_BENEATH` y `RESOLVE_NO_SYMLINKS`. Requiere Linux 5.6+; en kernels sin `openat2` la lectura falla de forma segura.
- En Windows todavía está pendiente la defensa equivalente para reparse points de directorios intermedios. Usa únicamente raíces locales de confianza.
- El cliente impone un límite de descarga de 512 MiB por defecto; puedes cambiarlo con `client.set_max_body_bytes(n)`. Al producirse un fallo, **el archivo de destino puede quedar parcial**: no lo utilices antes de verificar el resultado.

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

## Empaquetado de la API como lib1

`main.bg` y `client.bg` son ejemplos ejecutables; no deben formar parte del
paquete de biblioteca. `library.bg` es la entrada pública. Se genera un
árbol fuente temporal aislado para impedir colisiones del símbolo `main`:

```sh
python3 scripts/build_lib.py
bagron verify build/net.lib
```

Instala `build/net.lib` entre las bibliotecas que puede encontrar Bagron. Un
proyecto consumidor importa la clase de la biblioteca:

```bg
library net as Net
import { HttpClient } from Net

@unsafe
func main() int32:
    client: HttpClient = HttpClient(10000, 5, true)
    client.set_max_body_bytes(67108864)
    return 0
```

La biblioteca `net.lib` instalada y las bibliotecas nativas `gnulibrary.lib`,
`windows.lib` y `string.lib` deben proceder de fuentes compatibles con este
cambio. Los binarios precompilados anteriores pueden no incluir la API necesaria.

## Pruebas y estado de la release

- `bagron test_url.bg` verifica ocho casos de esquemas URL.
- `bagron test_headers.bg` verifica once casos de encuadre HTTP.
- `tests/integration_http.py` prueba cliente y servidor usando loopback, sin
  acceder a Internet (ver `tests/README.md`).
- `scripts/check_layout.py` verifica que Net no redeclare ABI nativa; GitHub
  Actions lo ejecuta en Linux y Windows. **Esto no sustituye pruebas binarias
  en Windows**, que siguen pendientes.
- `docs/ROADMAP.md` registra las fases completadas y los bloqueos de Net 1.1.0.

El compilador Bagron 1.1.4 necesita el ajuste local de relocalización PIC en
Linux para ciertos paquetes. Hasta incorporarlo a la release oficial, la
compilación y ejecución pueden requerir ese parche del backend LLVM.
