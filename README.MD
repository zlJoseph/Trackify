# 🛰️ Trackify - Backend

Trackify es un proyecto backend construido con **FastAPI**, **RabbitMQ**, **PostgreSQL**, y sigue los principios de **arquitectura hexagonal**, **CQRS** y **event-driven architecture**.

---

## 📁 Estructura del Proyecto

```
trackify/
├── contexts/
│   ├── users/
│   │   ├── application/
│   │   ├── domain/
│   │   ├── infrastructure/
│   ├── auth/
│   │   ├── application/
│   │   ├── domain/
│   │   ├── infrastructure/
├── interfaces/
│   ├── api/
│   │   └── routes/
│   │   └── middlewares/
│   │   └── schemas/
│   ├── consumers/
│   │   └── rabbitmq/
│   └── middleware/
├── shared/
│   ├── config/
│   ├── infrastructure/
├── tests/
├── .docker/
│   └── resources/
│       └── start.sh
│   └── Dockerfile
├── main_consumer.py
└── docker-compose.yml
```

- `contexts/`: Contiene los **bounded contexts** (`users`, `auth`), cada uno con su capa `application`, `domain` e `infrastructure`.
- `interfaces/`: Entrada/salida del sistema: api(rutas, middlewares y validadores) y consumidores de eventos
- `shared/`: Configuraciones comunes entre contextos.
- `.docker/` y `.docker/resources`: Configuraciones necesarias para ejecutar el proyecto en contenedores.
- `main_consumer.py`: Inicia los consumidores de eventos.

---

## 🚀 Cómo ejecutar el proyecto

### 📦 Requisitos

- Docker + Docker Compose

### 🔧 Variables de entorno

Configura un archivo `.env` en la raíz del proyecto. Puedes guiarte de `.env.example`:

```env
DB_HOST=postgres
DB_PORT=5432
DB_DATABASE=trackify
DB_USER=postgres
DB_PASSWORD=secret

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VHOST=/

JWT_SECRET=supersecretjwt
```

### ▶️ Levantar la app

```bash
docker compose up --build -d
```

Esto levantará:

- FastAPI (puerto `8000`)
- RabbitMQ (puerto `5672`)
- PostgreSQL (puerto `5432`)

El script `start.sh` se encarga de ejecutar las migraciones y levantar tanto la app como los consumidores de eventos.

### ✅ Ejecutar las migraciones

Las migraciones se debej ejecutar manualmente:

```bash
docker compose exec app alembic upgrade head
```

---

## 🧪 Ejecutar pruebas

Las pruebas usan `pytest`. Puedes ejecutarlas con:

```bash
docker compose exec app pytest tests/
```

---

## 🧱 Decisiones arquitectónicas

### 🔄 Arquitectura Hexagonal

- Separación clara entre **dominio**, **aplicación** e **infraestructura**.
- Las entidades y lógica de negocio no dependen de frameworks externos.
- Se utilizan interfaces para abstraer la persistencia y transporte.

### 📤 CQRS + Event Driven

- **Commands** para mutaciones (`CreateUserCommand`).
- **Queries** (lecturas) separadas, accediendo directamente a la tabla de lectura.
- **Eventos de dominio** propagados vía **RabbitMQ** (ej. `UserCreatedEvent`).
- Cada consumidor maneja su propio fallo y reintentos (con DLQ).

### 🔐 Seguridad

- Autenticación JWT con middleware personalizado para verificar y validar expiración.
- Cada contexto maneja sus propias excepciones y validaciones.

---

## 📬 Endpoints principales

| Método | Endpoint      | Descripción            |
| ------ | ------------- | ---------------------- |
| POST   | `/auth`       | Login de usuario (JWT) |
| POST   | `/users`      | Crear un usuario       |
| GET    | `/users/{id}` | Obtener usuario por ID |

### 📝 Ejemplo de body para `POST /users`

```json
{
  "first_name": "José Omar",
  "last_name": "Vegas",
  "middle_name": "Carrillo",
  "email": "omar41_41@hotmail.com",
  "password": "Probando@1",
  "gender": "M",
  "age": 26
}
```

---

## 🧠 Consideraciones finales

- Soporte completo para pruebas unitarias y de integración.
- Alto desacoplamiento entre capas.
- Cada contexto puede evolucionar de forma independiente.
- Docker-ready para despliegue local o CI/CD.
