# Módulo de Simulación y Gestión Bancaria (Odoo ERP / Python) 🏦

Este proyecto es un módulo nativo para **Odoo ERP** desarrollado en **Python**, enfocado en la gestión bancaria y transaccional. Implementa una arquitectura estricta basada en el patrón **MVC (Modelo-Vista-Controlador)** propio del ecosistema de Odoo, aplicando fuertemente los principios de la Programación Orientada a Objetos (POO) para garantizar la seguridad e integridad de los datos financieros.

## 🚀 Funcionalidades Principales

* **Modelado de Negocio:** Definición robusta de las estructuras de datos (Cuentas, Transacciones) utilizando el ORM de Odoo.
* **Seguridad y Accesos:** Configuración de listas de control de acceso (ACLs) y reglas de seguridad para restringir operativas críticas.
* **Vistas Personalizadas:** Interfaz de usuario integrada en el ERP mediante vistas XML (formularios, listados y menús de cuenta).
* **Control Transaccional:** Lógica de validación estricta para evitar saldos en descubierto y asegurar la trazabilidad de cada movimiento.

## 🛠️ Stack Tecnológico & Arquitectura

* **Lenguaje:** Python 🐍
* **Ecosistema:** Odoo ERP (Framework nativo)
* **Interfaz y Estructura:** XML para la capa de vistas.
* **Persistencia:** PostgreSQL (a través del ORM de Odoo).

## 📁 Estructura del Módulo

El desarrollo sigue rigurosamente el estándar de empaquetado de addons de Odoo:

* `models/`: Clases de Python que definen los modelos de datos y la lógica de negocio central mediante herencia de `models.Model`.
* `views/`: Archivos XML con la definición de la interfaz de usuario (`accountMenu`, formularios y acciones).
* `controllers/`: Controladores para gestionar rutas HTTP y peticiones web específicas.
* `security/`: Definición de grupos de usuarios y permisos de acceso (`ir.model.access.csv`).
* `demo/`: Datos de demostración para facilitar pruebas funcionales del módulo.
* `__manifest__.py`: Descriptor técnico del módulo, dependencias y carga de recursos.
* `__init__.py`: Inicializadores del paquete en Python.
