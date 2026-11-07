# Cambios de Bagron Net

## Cambios en desarrollo (sin release)

- Net delega sockets, DNS, E/S nativa y HTTPS en `windows` y
  `gnulibrary`, sin declaraciones `extern` propias.
- `OpenTcpHost` recorre los candidatos DNS y `ReuseAddress` permite
  reiniciar servidores de escucha sin esperar el cierre del puerto.
- Linux: lecturas del servidor restringidas al document root mediante
  `openat2` y rechazo de symlinks, con fallback seguro de denegación.
- Cliente HTTP: parser independiente para `Content-Length` y
  `Transfer-Encoding`, comprobaciones de encuadre ambiguo, y respuesta
  de tamaño cero sin espera innecesaria.
- `Location` solo se reconoce como nombre exacto de cabecera.
- Las escrituras de archivo controlan operaciones parciales.
- `HttpClient.set_max_body_bytes()` impone un máximo configurable; por
  defecto son 512 MiB. HTTPS también aplica límites de tamaño.
- `library.bg` y `scripts/build_lib.py` producen una biblioteca
  importable sin empaquetar los `main()` de los ejemplos.
- Tests de cabeceras, integración localhost, empaquetado y análisis
  estático para CI añadidos.
- Windows, TLS y limpieza atómica de descargas parciales continúan
  pendientes de validación o implementación; ver `docs/ROADMAP.md`.


## API orientada a objetos

- Se eliminaron las fachadas globales provisionales `download()` y `serve()`.
- Se añadieron `HttpClient` y `HttpServer` con configuración explícita.
- El servidor incorpora `GET`, `HEAD`, `index.html`, MIME básico, límites de
  solicitud y protección contra traversal.
- Los resultados de red se centralizaron en `result.bg`.
- El transporte de Windows y Linux incluye timeouts de socket.
- El cliente HTTP acepta `Content-Length` y `Transfer-Encoding: chunked`,
  sigue redirecciones con límite y soporta literales IPv4/IPv6.
- `HttpClient.head()` permite validar recursos HTTP sin escribir el cuerpo.
- El servidor admite binding IPv4 e IPv6 para loopback y wildcard.
