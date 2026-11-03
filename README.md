# net

**net** es una biblioteca de redes para el lenguaje de programación [Bagron](https://github.com/GrandKenzy/Bagron). Su propósito es proporcionar una interfaz nativa, clara y extensible para desarrollar aplicaciones que se comuniquen mediante redes, desde clientes TCP hasta servicios y servidores.

**Versión:** 1.0.0  
**Versión compatible de Bagron:** 1.0.3  
**Estado:** Desarrollo activo  
**Lenguaje:** Bagron

## Descripción

net busca facilitar el trabajo con conexiones de red sin renunciar al control de bajo nivel que ofrece Bagron. La biblioteca está desarrollada en Bagron y utiliza las interfaces nativas del sistema operativo para acceder a los servicios de red.

Su diseño prioriza:

- Una API coherente y sencilla para crear y administrar conexiones.
- Acceso explícito a sockets y operaciones de envío y recepción.
- Gestión predecible de recursos y errores.
- Transferencia de datos por bloques, sin necesidad de cargar archivos completos en memoria.
- Una base modular para ampliar el soporte de protocolos y plataformas.

## Funcionalidades

La implementación inicial se centra en las siguientes capacidades:

| Área | Alcance |
| --- | --- |
| Sockets | Creación, conexión y cierre de sockets. |
| Clientes TCP | Establecimiento de conexiones y comunicación con servicios remotos. |
| Transferencia de datos | Envío y recepción de información mediante operaciones nativas. |
| Gestión de errores | Consulta de errores proporcionados por la API de red del sistema. |
| Servidores | Desarrollo de herramientas para aceptar y administrar conexiones entrantes. |

Las funcionalidades disponibles pueden evolucionar durante el desarrollo de la biblioteca. Esta descripción no implica que todas las interfaces estén completas o estabilizadas.

## Compatibilidad

net 1.0.0 es compatible con **Bagron 1.0.3**.

El desarrollo inicial utiliza **Winsock2 en Windows**, mediante la interoperabilidad nativa de Bagron. La compatibilidad con otras plataformas y el alcance definitivo de sus API se documentarán conforme se incorporen y validen.

## Arquitectura

net mantiene separadas las responsabilidades de inicialización del subsistema de red, gestión de sockets y transferencia de datos. Esta separación permite reutilizar los servicios de red entre múltiples conexiones y desarrollar abstracciones de nivel superior sin ocultar el funcionamiento de las API nativas.

## Instalación y uso

Este repositorio está destinado al código fuente y la documentación de net. Las instrucciones de instalación, los ejemplos de uso y la referencia pública de la API se incorporarán junto con la implementación correspondiente.

Para conocer el lenguaje y sus herramientas, consulta el [repositorio oficial de Bagron](https://github.com/GrandKenzy/Bagron).

## Contribuciones

Las contribuciones son bienvenidas, especialmente las relacionadas con pruebas, compatibilidad, documentación y bibliotecas de protocolos. Antes de proponer cambios, se recomienda abrir una incidencia para describir el problema o la mejora y acordar su alcance.

Toda contribución de código debería incluir pruebas pertinentes y documentación de las interfaces públicas que introduzca o modifique.

## Proyecto

**net** forma parte del ecosistema de herramientas y bibliotecas desarrolladas para Bagron.

- **Repositorio:** [GrandKenzy/net](https://github.com/GrandKenzy/net)
- **Lenguaje:** [Bagron](https://github.com/GrandKenzy/Bagron)
- **Versión de net:** 1.0.0
