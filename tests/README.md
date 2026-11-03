# Pruebas de Bagron Net

Estas comprobaciones verifican los contratos públicos de net. Los ejemplos
se compilan con una instalación de Bagron compatible (1.0.3).

## Regresiones de URL (Bagron puro)

Compila y ejecuta `tests/test_url.bg`. Su código de salida es `0` si los
ocho casos pasan, o el número del caso fallido si alguno no coincide.

Casos cubiertos: `http://`, `https://`, `ftp://`, esquemas falsos con
prefijo `httpx://`, `httpsx://`, `ftpplus://`, separadores inválidos
y esquemas desconocidos.

## Cliente y servidor

1. Compilar `main.bg` como servidor HTTP local (puerto 8000) y `client.bg`
   como cliente. Ejecutar el servidor desde el directorio raíz de net.
2. Comprobar `GET /main.bg`, `HEAD /main.bg` y `HttpClient.head()`.
3. Solicitar un archivo inexistente: debe responder `404`.
4. Solicitar `/../main.bg` y `/%2e%2e/main.bg`: deben responder `403`.
5. Comprobar que el cliente descarga el archivo con el contenido correcto.
6. Usar una respuesta `Transfer-Encoding: chunked` dividida entre varias
   lecturas; verificar que no quedan tamaños hexadecimales ni trailers.
7. Repetir con IPv6 `::1` y consultar `http://[::1]:8000/main.bg`.

## Regresiones de robustez

- **Redirección entre esquemas:** responder `302` con `Location:`
  absoluta `https://...`. El cliente debe utilizar el backend HTTPS y
  guardar el cuerpo de la respuesta final.
- **Redirección inválida:** responder `302` sin `Location`; el cliente
  debe fallar sin interpretar una URL no inicializada.
- **Desbordamiento:** responder con `Content-Length: 2147483648`; el
  cliente debe rechazar la cabecera con `NET_HEADER`.
- **Cabecera malformada:** responder con `Content-Length: 12abc`; el
  cliente debe rechazarla con `NET_HEADER`.
- **Recepción interrumpida:** cerrar o forzar error de socket tras la
  apertura del archivo. Comprobar que el descriptor se libera.
- **Timeout HTTPS Linux:** conectar a un servidor TLS de prueba que retenga
  la respuesta más allá del límite configurado; esperar `NET_TIMEOUT`.
- **Enlaces simbólicos:** crear un enlace interno a un archivo exterior al
  directorio servido y comprobar la política de acceso. **Este caso sigue
  pendiente de endurecimiento:** no ejecutar el servidor con raíces no
  confiables hasta resolverlo.

La suite de integración puede utilizar un cliente TCP del sistema para enviar
bytes HTTP específicos; no necesita Python como dependencia de la aplicación.

> Estado: lista de pruebas de regresión. La presencia de un caso aquí no
> significa que se haya ejecutado o aprobado automáticamente.
