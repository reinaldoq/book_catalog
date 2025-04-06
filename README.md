# Book Catalog API

A RESTful API built with **Django** and **Django Rest Framework (DRF)** for managing a digital catalog of books. The system supports two user roles: **Editors** (content creators) and **Readers** (content consumers). It includes full CRUD functionality, user registration, authentication via JWT, RBAC-based permissions, and auto-generated OpenAPI documentation.

---

## 🚀 Features

- **User management** with registration for readers and admin-only full CRUD.
- **JWT authentication** via [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/).
- **Role-based access control**:
  - Editors can create/update/delete books.
  - Readers can only view books and delete their own account.
- **Books API** with paginated list, detail view, and search support.
- **Auto-generated API docs** via [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/).
- **Django Admin** interface for managing users and books.
- **Dockerized** setup using MySQL-compatible backend (MariaDB).
- **Test suite** using `pytest`, `Factory Boy`, and Django's `TestCase`.

---

## 👷️ Creating an Admin User

Once the containers are running:

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompt to provide an email, username, and password.

---

## 🌐 Accessing Django Admin

You can log in at:

```
http://localhost:8000/admin/
```

Use the credentials from the `createsuperuser` command above.

---

## 🔍 API Documentation

This project uses **drf-spectacular** to generate OpenAPI schema + Swagger UI.

- OpenAPI schema: [`/api/schema/`](http://localhost:8000/api/schema/)
- Swagger UI: [`/api/docs/`](http://localhost:8000/api/docs/)

---

## 💡 Application Overview

### Users

- `POST /api/users/` — Public registration (role=reader only)
- `GET|PATCH|DELETE /api/users/<uuid>/` — Admin-only (except DELETE if self)

### Authentication

- `POST /api/token/` — Get JWT access & refresh tokens
- `POST /api/token/refresh/` — Refresh access token

### Books

- `GET /api/books/` — List all books (paginated)
- `POST /api/books/` — Editor only
- `GET /api/books/<uuid>/` — Retrieve book details
- `PATCH|DELETE /api/books/<uuid>/` — Editor only

---

## 📄 Test Coverage

Implemented with `pytest` and Django's `TestCase`. Tests cover:

- User registration and admin-only permissions
- Reader's ability to delete their own account only
- Full CRUD operations for books (editor only)
- Read-only book access for reader users
- Authenticated vs unauthenticated access paths
- JWT authentication flow
- Permission checks for all endpoints

Factories are provided for both `Reader` and `Editor` users using **Factory Boy**.

---

## ⚙️ Tech Stack

- **Django 4.2**
- **Django REST Framework**
- **drf-spectacular** for schema/docs
- **SimpleJWT** for authentication
- **MySQL/MariaDB** for relational DB
- **Docker** for containerized development
- **pytest**, **Factory Boy**, **model-utils** for testing

---

## 🌐 Running the Project

```bash
docker-compose up --build
```

Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)\
Docs: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## 📊 Tarea 2: Escalabilidad

### 1. ¿Cómo gestionarías esta cantidad de datos a nivel técnico?

Para manejar eventos de lectura con un millón de usuarios simultáneos:

- Separaría los servicios críticos (API de libros y usuarios) del sistema de eventos.
- Usaría una arquitectura orientada a eventos con **Kafka** o **Amazon Kinesis** para procesar eventos de lectura en tiempo real.
- Utilizaría un **sistema de colas** como **Celery + Redis** o **Kafka consumers** para procesar los eventos de forma asíncrona.
- Agregaría **autoescalado** en la infraestructura (k8s, ECS, etc.) según carga.
- Emplearía particionado horizontal (sharding) en bases de datos si es necesario.

### 2. ¿Qué tipo de base de datos utilizarías para almacenar las métricas de lectura de los usuarios? ¿Por qué?

Usaría una base de datos **orientada a series de tiempo** como:

- **TimescaleDB** (extensión de PostgreSQL)
- **ClickHouse** (alto rendimiento analítico)
- **InfluxDB** (si las métricas son simples y necesitan ingestón rápida)

Estas bases permiten:

- Ingestar grandes volúmenes de datos de forma eficiente.
- Consultas agregadas por ventana de tiempo.
- Almacenamiento optimizado por compresión.

### 3. ¿Has trabajado con alguna base de datos o infraestructura que soporte un volumen alto de usuarios y datos? Si es así, cuéntanos tu experiencia y qué tecnologías utilizaste.

Sí, he trabajado en sistemas que procesaban millones de eventos al día para una app de movilidad (tipo Uber):

- En un proyecto de IoT, usamos **TimescaleDB** + **PostgreSQL** para registrar métricas de sensores en tiempo real.
- Implementamos **AWS Kinesis** y **AWS Lambda** para ingerir eventos desde dispositivos.
- Usamos **S3** para almacenar datos fríos y **Redshift** para agregación y reporting, como un datalake.
- La arquitectura estaba orquestada con **Docker + ECS**, escalando workers según demanda.



---

## ☁️ Tarea 3: AWS y Despliegue

### Despliegue en Amazon ECS (Elastic Container Service)

#### Pasos que recomendaria  para desplegar la aplicación:

1. Construcción de imágenes Docker con `Dockerfile` y subida a un repositorio privado en **Amazon ECR**.
2. Creación de una base de datos **RDS MariaDB** con los mismos parámetros de configuración. Honestamente, yo preferiria usar PostgresSQL para todo el poyecto y RDS en AWS.
3. Definición de una **task definition** en ECS Fargate con variables de entorno para conectar con la base de datos.
4. Creación de un **servicio ECS** vinculado a un **Application Load Balancer (ALB)**.
5. Configuración de una **VPC pública con subredes públicas** para exponer la aplicación.
6. Uso de **AWS Secrets Manager** para variables sensibles como `MYSQL_PASSWORD`, `SECRET_KEY`, etc.
7. Configuración del dominio con **Route 53** para acceso por nombre de dominio.

#### Configuraciones importantes:

- ECS Fargate (sin necesidad de administrar servidores)
- CPU/memoria autoescalable por tráfico
- Health checks configurados en el Load Balancer
- Logs enviados a **CloudWatch Logs** para monitoreo

#### Cómo acceder a la aplicación desplegada:

- Se accede por el dominio configurado, por ejemplo:

```
https://book-catalog.fictionexpress.com
```

- Swagger UI: `https://book-catalog.fictionexpress.com/api/docs/`
- Django admin: `https://book-catalog.fictionexpress.com/admin/`
