# Cambios de Bagron Net

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
