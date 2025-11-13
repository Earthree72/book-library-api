# 📚 Book Library API

## 🧾 Project Description
The **Book Library API** is a simple RESTful API built with **Python** and **Flask**.  
It allows users to manage a collection of books — including viewing, adding, updating, and deleting records.  
This project demonstrates basic API design principles and CRUD (Create, Read, Update, Delete) operations.  
All book data is temporarily stored in memory while the application is running.

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| **GET** | `/books` | Retrieve all books |
| **GET** | `/books/<id>` | Retrieve a single book by its ID |
| **POST** | `/books` | Add a new book |
| **PUT** | `/books/<id>` | Update an existing book by ID |
| **DELETE** | `/books/<id>` | Delete a book by ID |

---

## ⚙️ Setup Instructions

1. **Clone this repository:**
   ```bash
   git clone https://github.com/<your-username>/book-library-api.git
   ```

2. **Navigate into the project folder:**
   ```bash
   cd book-library-api
   ```

3. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

   Activate it:
   - **Windows:**
     ```bash
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:**
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

6. **Access the API in your browser or API testing tool (e.g. Postman):**
   ```
   http://127.0.0.1:5000
   ```

---

## 🧪 Example API Calls

### ✅ Get All Books
```bash
curl http://127.0.0.1:5000/books
```

### ✅ Get a Single Book
```bash
curl http://127.0.0.1:5000/books/1
```

### ✅ Add a New Book
```bash
curl -X POST -H "Content-Type: application/json" \
-d "{\"title\": \"The Great Gatsby\", \"author\": \"F. Scott Fitzgerald\"}" \
http://127.0.0.1:5000/books
```

### ✅ Update a Book
```bash
curl -X PUT -H "Content-Type: application/json" \
-d "{\"author\": \"George Orwell (Updated)\"}" \
http://127.0.0.1:5000/books/1
```

### ✅ Delete a Book
```bash
curl -X DELETE http://127.0.0.1:5000/books/2
```

---

## 🧰 Technologies Used
- **Python 3.x**
- **Flask** (for handling API routes)
- **cURL / Postman** (for testing endpoints)
- **JSON** (for data formatting)

---

## 🧠 Notes
- All data is stored in memory only; restarting the server resets the book list.
- For persistence, consider saving data to a JSON file or using a database (e.g. SQLite, PostgreSQL).
- You can modify the `books` list directly in `app.py` to pre-load more book records.
