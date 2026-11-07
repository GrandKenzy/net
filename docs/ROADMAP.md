# Plan de estabilización de Net 1.1.0

Estado revisado: 2026-11-07. La versión publicada en package.toml sigue siendo
1.0.0; estos cambios **no** constituyen una release estable 1.1.0.

## Fase 1 — ABI compartida (parcial)
- [x] Eliminar los externs duplicados de Net.
- [x] Centralizar TCP, DNS y opciones de sockets en gnulibrary/windows.
- [x] Mantener los tipos de archivo separados de los de socket.
- [x] Compilar y probar el transporte en Linux x86_64.
- [ ] Compilar y probar nativamente todo el flujo Windows x64.

## Fase 2 — TCP robusto (parcial)
- [x] Probar todas las direcciones de getaddrinfo antes de fallar.
- [x] Cerrar correctamente el socket de cada intento fallido.
- [x] Añadir ReuseAddress para reiniciar listeners.
- [x] En Linux, Send utiliza MSG_NOSIGNAL desde gnulibrary.
- [ ] Timeout real para connect bloqueante, con conexión nonblocking y espera.
- [ ] Revisar EOF, EINTR, EAGAIN y vida útil de punteros de dirección.
- [ ] Tests de IPv6 y simultaneidad.

## Fase 3 — Cliente HTTP/1.1 (parcial)
- [x] Parser estricto para Content-Length y Transfer-Encoding: chunked.
- [x] Rechazo de encuadre duplicado/contradictorio.
- [x] Content-Length: 0 sin esperar EOF.
- [x] Coincidencia exacta del encabezado Location.
- [x] Soporte de escrituras parciales y límite configurable de descarga.
- [ ] Descargar a archivo temporal seguro y reemplazar atómicamente al terminar.
- [ ] Limitar la longitud total de trailers y resolver redirects relativos.
- [ ] Manejar explícitamente errores de timeout y cerrar archivos en cada ruta.

## Fase 4 — Servidor seguro (parcial)
- [x] Linux: openat2 con RESOLVE_BENEATH | RESOLVE_NO_SYMLINKS.
- [x] Prueba de symlink externo y de rutas ../: HTTP 403.
- [x] Reutilización de puerto tras cerrar conexiones.
- [ ] Windows: verificar el árbol real mediante handles/canonicalización segura.
- [ ] Cancelación cooperativa de accept(), mitigación Slowloris y concurrencia.
- [ ] Documentar fallos seguros en Linux anteriores a openat2 (5.6).

## Fase 5 — HTTPS (parcial)
- [x] Conservar libcurl/WinHTTP dentro de las bibliotecas nativas.
- [x] Límite de descarga en libcurl y WinHTTP.
- [ ] Tests TLS válidos e inválidos en Linux/Windows.
- [ ] Política uniforme de redirects, límites y métodos HEAD.
- [ ] Separar libcurl opcionalmente del paquete base gnulibrary.

## Fase 6 — API y empaquetado (parcial)
- [x] Separar library.bg de los ejemplos main.bg/client.bg.
- [x] Crear scripts/build_lib.py para empaquetar solo la API.
- [x] Verificar net.lib e importarlo desde un proyecto ajeno.
- [ ] API pública de buffers/streams; normalización de códigos de error.

## Fase 7 — Pruebas y publicación (parcial)
- [x] 11 regresiones de encuadre y 8 pruebas de cliente en Linux.
- [x] 4 regresiones de servidor en Linux.
- [x] Comprobaciones estáticas en Linux/Windows mediante Actions.
- [ ] Tests de compilación/ejecución en CI con Bagron instalado para ambas OS.
- [ ] Regenerar y publicar las bibliotecas precompiladas de BagronLab.
- [ ] Changelog, release candidates y artefactos firmados de Net 1.1.0.

## Criterio de lanzamiento

**No publicar Net 1.1.0 como estable** hasta cerrar las casillas de
seguridad, TLS y pruebas Windows, comprobar que la versión de Bagron instalada
contiene el arreglo de relocalizaciones PIC para Linux, y ejecutar la suite
contra los paquetes de distribución (no solo contra fuentes).

Aviso: la política de nombres de ruta de Windows sigue sin bloquear los
reparse points intermedios. Mantener el servidor restringido a pruebas locales
con directorios de confianza hasta corregirlo.
