Here’s your updated `README.md` with the **new updates integrated**—including:

* The system now uses **file-based storage** (`data.txt`, `signup.txt`)
* `main.py` file is included
* Future plan to migrate to a database is retained
* Minor fixes for link formatting and consistency

---

```markdown
# 🛠 Help Desk System

A complete ticket management platform built using **Flask**, designed to simplify issue reporting, tracking, and resolution for organizations. It includes user authentication, priority marking, admin dashboards, department views, email notifications, and persistent storage via files.

[🌐 View Live Site](https://hdesk.onrender.com)

---

## 🚀 Features

- 📝 Ticket submission with subject, department, date, time, and location  
- 🔐 User signup/sign-in system (SSN-verified emails)  
- 📊 Admin dashboard with:
  - Priority marking  
  - Ticket status updates  
  - Sorting & searching  
  - Department-wise filtering  
- 📬 Email notifications for ticket creation and closure using Gmail SMTP  
- 📂 Data stored and retrieved from `data.txt` and `signup.txt` files  
- 🌐 Flask-based frontend using Jinja2 templates  

---

## 🧰 Tech Stack

- **Backend**: Python, Flask, Flask-Mail  
- **Frontend**: HTML, CSS, Jinja2  
- **Storage**: Text files (`data.txt`, `signup.txt`)  
- **Email**: Gmail SMTP integration  
- **Other Libraries**: `random`, `re`, `datetime`  

---

## 📁 Project Structure

```

helpdesk-system/
│
├── templates/                   # All HTML templates
│   ├── home.html
│   ├── signin.html
│   ├── signup.html
│   ├── submit.html
│   ├── admin\_dashboard.html
│   ├── dashboard.html
│   ├── details.html
│   ├── opened1.html
│   ├── closed1.html
│   ├── departments.html
│   └── department\_tickets.html
│
├── app.py                       # Main Flask application
├── main.py                      # Alternate or extended version
├── data.txt                     # Stores all tickets
├── signup.txt                   # Stores user signup credentials
├── requirements.txt             # Required dependencies
└── README.md                    # Project documentation

````

---

## 🧑‍💻 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/helpdesk-system.git
cd helpdesk-system
````

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the server

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 📦 Dependencies (From `requirements.txt`)

Some key packages:

* `Flask`
* `Flask-Mail`
* `Jinja2`
* `Werkzeug`
* `python-dateutil`
* `pytest` (for testing)
* `supabase`, `httpx`, `Twisted` (if used in extensions)

---

## 🌟 Future Enhancements

* ✅ Add database integration (e.g., PostgreSQL or MongoDB)
* 📱 Make UI fully responsive
* 📈 Export reports as PDF or CSV
* 🧾 Add ticket history or comment thread

---

## 👨‍💻 Author

**Vihashni R**
🔗 GitHub: [vihashni08](https://github.com/vihashni08)

```

