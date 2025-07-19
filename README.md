# 💼 dioBank – Banking API with FastAPI

This project is a study case using FastAPI to build a simple banking API with asynchronous operations, JWT authentication, and a clean layered architecture.

---

## 🚀 Technologies

- [FastAPI](https://fastapi.tiangolo.com/) – High-performance web framework
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [Databases](https://www.encode.io/databases/) – Async database layer
- [PostgreSQL](https://www.postgresql.org/) – Relational database
- [JWT](https://jwt.io/) – Authentication via JSON Web Tokens
- [Poetry](https://python-poetry.org/) – Dependency management

---

## 🧱 Project Structure

```bash
dioBank/
├── src/
│   ├── controllers/       # API routes
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── views/             # views
│   ├── database.py        # DB connection config
│   └── main.py            # Application entry point
├── README.md
└── pyproject.toml
```

---

## 🔐 Authentication

Authentication is handled via **JWT**.  
To access protected routes, you must log in and use the token received.

### 📥 Login

```http
POST /auth/login
```

### 🔑 Use token in your requests

```http
Authorization: Bearer <your_token>
```

---

## 📌 Main Endpoints

### 🧾 Accounts

```http
GET /bank/read_accounts?limit=10&skip=0
GET /bank/read_account/{id}
POST /bank/create_account
```

### 💰 Transactions

```http
POST /bank/create_transaction/{id_account}
GET /bank/read_transactions/{id_account}
```

---

## ▶️ How to Run

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run the server
uvicorn src.main:app --reload
```

---

## ✅ To-Do (Next Improvements)

- [ ] Add automated tests
- [ ] Improve Swagger docs
- [ ] Add statement filtering by period
- [ ] User roles and permissions
- [ ] Architecture documentation