# Pruebas de Bagron Net

Estas pruebas se dividen en compilación rápida e integración agresiva.

## Compilación rápida

Desde la raíz de Bagron:

```powershell
vnma run main.py "C:\Users\Kentucky\Desktop\utilities\App Bagron\net\main.bg" -o "C:\Users\Kentucky\Desktop\utilities\App Bagron\net\build\server.exe"
vnma run main.py "C:\Users\Kentucky\Desktop\utilities\App Bagron\net\client.bg" -o "C:\Users\Kentucky\Desktop\utilities\App Bagron\net\build\client.exe"
```

## Integración

1. Ejecutar `build/server.exe` con el directorio de trabajo `net/`.
2. Comprobar `GET /main.bg`, `HEAD /main.bg` y `HttpClient.head()`.
3. Comprobar `404` para un archivo inexistente.
4. Enviar literalmente `/../main.bg` y `/%2e%2e/main.bg`; ambas deben devolver
   `403`.
5. Ejecutar `build/client.exe` contra el servidor y verificar el archivo
   descargado.
6. Usar un servidor TCP de prueba que entregue una respuesta chunked partida
   entre varias lecturas; el archivo resultante debe reconstruir el cuerpo sin
   los tamaños hexadecimales ni los trailers.
7. Repetir la integración con `HttpServer` configurado con `::1` y consultar
   `http://[::1]:8000/main.bg`.

La prueba de redirección debe comprobar dos conexiones: una respuesta `302`
con `Location` absoluta y una respuesta final `200`. El límite de
`max_redirects` debe devolver `NET_REDIRECT` cuando se supera.

La prueba agresiva usa un cliente TCP del sistema para conservar exactamente
los bytes de la solicitud y no depende de Python.
