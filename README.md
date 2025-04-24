# PricePulse


## 1.Introduction

The project PricePulse is a software that aims to provide updated prices to the vendors of the distribuitor in real time.

## 1.1 Purpose

The purpose of this document is to outline the requirements for the app that the vendors will be using daily. This document will be used by all stakeholders, developers and testers.

## 1.2 Scope

The scope of this project is limited to the testing of the features described in the succeding sections of this document.
Non-functional testing like stress, performance is beyond scope of this project.
Automation testing is beyond scope.
Functional testing and a basic external interface are in scope and need to be tested.

## 1.3 Definitions, Acronyms, and Abbrevations 
| Abbreviation | Word     |
|--------------|----------|
| A            | Admin    |
| D            | Distributor|
| D            | Developer|
| S            |Stakeholder|
| T            | Tester   |  
| V            | Vendor   |
## 2. Requirements

### 2.1 Roles Description

| Role         | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **Vendor**   | User of the mobile application. Queries product prices in real time.        |
| **Distributor** | Provides updated product data to be consumed by the app.                |
| **Admin**    | Manages user access and system configurations.                              |
| **Tester**   | Validates that the app behaves according to the specified requirements.     |
| **Developer**| Implements and maintains app features based on stakeholder input.           |

### 2.2 Features per Role

| Role         | Features                                                                                 |
|--------------|------------------------------------------------------------------------------------------|
| **Vendor**   | - Search product by code or name  <br> - View updated prices in real time                |
| **Admin**    | - Manage vendor accounts  <br> - Reset passwords  <br> - Monitor system status           |
| **Tester**   | - Execute functional test cases  <br> - Report bugs  <br> - Verify bug fixes             |
| **Developer**| - Develop backend API  <br> - Implement front-end components  <br> - Fix issues          |
| **Distributor** | - Feed price updates to the system  <br> - Ensure data accuracy                      |

### 2.3 User Stories 
#### User Story 1: Buscar productos por nombre o código

**Como** vendedor,  
**quiero** buscar productos por nombre o código  
**para** acceder rápidamente a la información del precio.

**Criterios de Aceptación**

- **Escenario 1 (Positivo):**  
  **Dado que** el vendedor está en la pantalla de búsqueda,  
  **cuando** introduce un código o nombre válido y presiona buscar,  
  **entonces** se muestra la información del producto y su precio.
- **Escenario 2 (Negativo):**  
  **Dado que** el vendedor introduce un código incorrecto,  
  **cuando** presiona buscar,  
  **entonces** se muestra un mensaje de “Producto no encontrado”.

---

#### User Story 2: Ver precios más recientes

**Como** vendedor,  
**quiero** tener la seguridad de que estoy viendo los precios más recientes  
**para** evitar vender con precios desactualizados.

**Criterios de Aceptación**

- Mostrar la fecha de última actualización junto al precio.
- Actualización automática de precios al abrir la pantalla o tras un intervalo predeterminado.

---

#### User Story 3: Cargar listas de precios

**Como** distribuidor,  
**quiero** poder cargar las nuevas listas de precios  
**para** mantener a mis vendedores actualizados.

**Criterios de Aceptación**

- Poder subir archivos de lista de precios en formatos como Excel (.xlsx, .xls) y CSV.  
- Validación de formato y datos (p. ej. columnas requeridas: código, nombre, precio).  
- Mostrar un mensaje de “Actualización exitosa” o, en caso de error, “Error al procesar el archivo” con detalles.  
- Registro de fecha y usuario que realizó la carga.


### 2.4 Test cases

####  User Story 1: Buscar productos por nombre o código
TestCase-1.1 - Búsqueda exitosa por nombre o código
Precondiciones: El usuario está en la pantalla de búsqueda

Pasos:
Ingresar un nombre o código válido en el campo de búsqueda
Presionar el botón “Buscar”.
Entrada: "123ABC" o "Coca Cola"
Resultado esperado: Se muestra la información del producto con su precio

TestCase-1.2 - Búsqueda con código inválido
Precondiciones: El usuario está en la pantalla de búsqueda

Pasos:
Ingresar un código inválido
Presionar el botón “Buscar”
Entrada: "ZZZ000"
Resultado esperado: Se muestra mensaje “Producto no encontrado”


#### User Story 2: Ver precios más recientes
TestCase-2.1 - Mostrar fecha de última actualización
Precondiciones: El usuario visualiza un producto

Pasos:
Ingresar al detalle de producto
Resultado esperado: Se muestra la fecha de última actualización del precio

TestCase-2.2 - Validar actualización automática
Precondiciones: La lista de precios fue actualizada en el servidor

Pasos:
Abrir la app con conexión a Internet
Esperar a que se cargue la información
Resultado esperado: Se muestran los precios actualizados automáticamente


#### User Story 3: Cargar listas de precios
TestCase-3.1 - Subir lista de precios (formato válido)
Precondiciones: El usuario tiene acceso de administrador

Pasos:
Subir archivo Excel válido
Presionar “Cargar”
Resultado esperado: Mensaje “Lista cargada exitosamente”

TestCase-3.2 - Subir lista de precios (formato inválido)

Pasos:
Subir un archivo con formato incorrecto o datos faltantes
Resultado esperado: Se muestra error con detalle del problema

### 3. Technical Specifications

#### 3.1 Arquitectura del Sistema

**Nota:** Esta sección será completada en futuras actualizaciones del documento.

La aplicación está compuesta por una base de datos central y dos interfaces diferenciadas según el perfil de usuario. Por un lado, se desarrollará una **aplicación web exclusiva para administradores**, quienes serán responsables de cargar y actualizar las listas de precios. Por otro lado, se implementará una **aplicación móvil destinada a los vendedores**, diseñada para facilitar la consulta rápida y actualizada de precios durante sus visitas a clientes.

Dado que la web app será utilizada únicamente por uno o dos administradores, y considerando que la API pública estará orientada a la distribución de la lista de precios para los vendedores, **no resulta necesario implementar un sistema complejo de autenticación y gestión de usuarios para la interfaz administrativa**. En este sentido, se optará por desarrollar una **API separada, restringida y segura**, exclusivamente para la administración de precios, evitando así exponer funcionalidades innecesarias a la red pública.


![Architecture diagram](./system_architecture.jpg)


#### 3.2 Definición de API

El sistema PricePulse expone una API RESTful que permite:

- A los **vendedores**, buscar productos por código o nombre y visualizar precios actualizados en tiempo real.  
- A los **distribuidores**, subir nuevas listas de precios para mantener la información actualizada.

La especificación completa de la API está definida utilizando el formato **OpenAPI (Swagger)** y puede consultarse en el siguiente documento: **[PricePulse API Contract]**.

**Endpoints principales:**

- `GET /products/search`  
  Permite a los vendedores buscar productos por nombre o código.  
  **Parámetros esperados:** `name` o `code`  
  **Respuesta:** Información del producto y precio actual

- `POST /price-lists/upload`  
  Permite a los distribuidores subir nuevas listas de precios.  
  **Formato permitido:** `.xlsx`, `.xls`, `.csv`  
  **Validaciones:** estructura del archivo, columnas requeridas (`code`, `name`, `price`), tipo de datos  
  **Respuesta:** Mensaje de éxito o detalle de errores

**Manejo de errores:**  
Las respuestas incluirán códigos HTTP estándar y mensajes detallados en caso de errores (por ejemplo, `400 Bad Request`, `500 Internal Server Error`).

Para más detalles sobre los parámetros de las peticiones, formatos de respuesta y ejemplos de uso, consultar el contrato de la API mencionado anteriormente.

