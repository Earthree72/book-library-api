# 📚 Book Library API (with JWT Authentication)

## 🧾 Project Description

The **Book Library API** is a RESTful API built using **Python** and **Flask**.
It allows users to manage a collection of books — including viewing, adding, updating, and deleting records.

In this version, the API now includes:

* 🔐 **User Registration**
* 🔑 **Login with JWT Authentication**
* 📁 **Persistent user and book storage** (using JSON files)
* 🛡️ **Ownership protection** — only the creator of a book can update or delete it

This project demonstrates API design, CRUD operations, authentication, authorization, and simple persistence without a database.

---

## 🔐 Authentication Features

The API uses **JWT (JSON Web Tokens)** for secure authentication.

### ✔ Register a New User

**POST** `/auth/register`
Body:

```json
{
  "username": "alice",
  "password": "12345"
}
```

### ✔ Login and Get a Token

**POST** `/auth/login`
Body:

```json
{
  "username": "alice",
  "password": "12345"
}
```

Response:

```json
{
  "access_token": "<your_jwt_token>"
}
```

### ✔ How to Use the Token

In Postman:

1. Go to **Authorization**
2. Set **Type** = Bearer Token
3. Paste the JWT token

---

## 🔗 API Endpoints

### 📘 Public Endpoints

| Method  | Endpoint      | Description           |
| ------- | ------------- | --------------------- |
| **GET** | `/books`      | Retrieve all books    |
| **GET** | `/books/<id>` | Retrieve a book by ID |

### 🔐 Protected Endpoints (Require JWT)

| Method     | Endpoint      | Description                               |
| ---------- | ------------- | ----------------------------------------- |
| **POST**   | `/books`      | Add a new book (authenticated users only) |
| **PUT**    | `/books/<id>` | Update a book (owner only)                |
| **DELETE** | `/books/<id>` | Delete a book (owner only)                |

---

## 🛡️ Ownership Rules

When a user creates a book:

* The book is assigned `"owner": "<username>"`

Only that user can:

* ✏️ **Update the book**
* ❌ **Delete the book**

If another user attempts to modify it:

```json
{ "error": "forbidden: you are not the owner" }
```

---

## 💾 Persistence

This project stores data in JSON files to survive application restarts:

* **users.json** — contains usernames and hashed passwords
* **books.json** — stores the book list with owner information

This fulfills the “persistent data structure” requirement without using a database.

---

## ⚙️ Setup Instructions

1. **Clone this repository:**

```bash
git clone https://github.com/<your-username>/my-new-book-api.git
```

2. **Navigate into the project folder:**

```bash
cd my-new-book-api
```

3. **(Optional) Create a virtual environment:**

```bash
python -m venv venv
```

Activate it:

* **Windows:**

```bash
.\venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

5. **Run the application:**

```bash
python app.py
```

6. **API will be available at:**

```
http://127.0.0.1:5000
```

---

## 🧪 Example API Calls (cURL)

### 🔒 Register

```bash
curl -X POST http://127.0.0.1:5000/auth/register \
-H "Content-Type: application/json" \
-d "{\"username\": \"alice\", \"password\": \"12345\"}"
```

### 🔑 Login

```bash
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d "{\"username\": \"alice\", \"password\": \"12345\"}"
```

### 📘 Get All Books

```bash
curl http://127.0.0.1:5000/books
```

### ➕ Add a Book (Requires Token)

```bash
curl -X POST http://127.0.0.1:5000/books \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d "{\"title\": \"New Book\", \"author\": \"Me\"}"
```

### ✏️ Update a Book (Owner Only)

```bash
curl -X PUT http://127.0.0.1:5000/books/3 \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d "{\"author\": \"Updated Author\"}"
```

### ❌ Delete a Book (Owner Only)

```bash
curl -X DELETE http://127.0.0.1:5000/books/3 \
-H "Authorization: Bearer <token>"
```

---

## 🧰 Technologies Used

* **Python 3.x**
* **Flask**
* **Flask-JWT-Extended**
* **Werkzeug Password Hashing**
* **JSON** for persistence
* **Postman / cURL** for testing

---

## 🧠 Notes

* Passwords are securely hashed before being stored.
* JWT is required for any modification to book data.
* `users.json` and `books.json` ensure data persists across application restarts.
* Ownership enforcement prevents unauthorized updates or deletions.

---

