from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db
from datetime import datetime
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from models import User, Ticket
from urllib.parse import quote
import random
import re
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
load_dotenv()

app.secret_key = os.getenv('SECRET_KEY')
password = quote(os.getenv('DB_PASSWORD'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost/helpdesk_db'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_USERNAME')
)
mail = Mail(app)
db.init_app(app)
# -------------------- Utility --------------------

def generate_ticket_id():
    return str(random.randint(100000, 999999))

# -------------------- Routes --------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signin')
def sign_in():
    return render_template('signin.html')

@app.route('/signup')
def signup_form():
    return render_template('signup.html')

@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']

    if not re.match(r"[a-zA-Z0-9._%+-]+@ssn.edu.in", email):
        flash('Invalid email. Please use an SSN email address.')
        return redirect(url_for('signup_form'))

    if User.query.get(email):
        flash('Account already exists. Please sign in.')
        return redirect(url_for('signup_form'))

    db.session.add(User(email=email, name=name, password=password))
    db.session.commit()
    flash('Signup successful. Please sign in.')
    return redirect(url_for('sign_in'))

@app.route('/submit_signin', methods=['POST'])
def submit_signin():
    email = request.form['email']
    password = request.form['password']

    if not email or 'ssn.edu.in' not in email:
        flash('Invalid email. Email must include "ssn.edu.in".')
        return redirect(url_for('sign_in'))

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        if email == 'admin@ssn.edu.in':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard', email=email))

    flash('Invalid email or password.')
    return redirect(url_for('sign_in'))

@app.route('/dashboard/<email>')
def dashboard(email):
    user = User.query.get(email)
    if not user:
        flash('User not found.')
        return redirect(url_for('sign_in'))
    user_tickets = Ticket.query.filter_by(email=email).all()
    return render_template('dashboard.html', name=user.name, email=email, tickets=user_tickets)

@app.route('/admin_dashboard')
def admin_dashboard():
    tickets = Ticket.query.order_by(Ticket.priority.desc()).all()
    return render_template('admin_dashboard.html', tickets=tickets)

@app.route('/submit_page')
def submit_page():
    return render_template('submit.html', ticket_id=generate_ticket_id(), current_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/submit_ticket', methods=['POST'])
def submit_ticket():
    try:
        print("🚀 Form data:", dict(request.form))
        formatted_date = request.form['date']  # Expected in dd/mm/yyyy
        ticket_id = generate_ticket_id()

        while Ticket.query.get(ticket_id):
            ticket_id = generate_ticket_id()

        user = User.query.get(request.form['email'])
        if not user:
            flash("Email not registered. Please sign up first.")
            return redirect(url_for('submit_page'))

        ticket = Ticket(
            id=ticket_id,
            name=request.form['name'],
            date=formatted_date,
            status='Opened',
            subject=request.form['subject'],
            department=request.form['department'],
            location=request.form['location'],
            room=request.form['room'],
            mobile=request.form['mobile'],
            time=request.form['time'],
            priority=False,
            email=request.form['email']
        )
        db.session.add(ticket)
        db.session.flush()
        db.session.commit()
        print("✅ Ticket submitted with ID:", ticket.id)

        send_email(ticket.email, ticket.id, ticket)

        return redirect(url_for('ticket_details', ticket_id=ticket.id))

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error submitting ticket: {e}")
        flash(f"❌ Failed to submit ticket: {e}")
        return redirect(url_for('submit_page'))

@app.route('/ticket/<ticket_id>')
def ticket_details(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        flash("❌ Ticket not found.")
        return redirect(url_for('submit_page'))
    return render_template('details.html', ticket=ticket)

@app.route('/opened_tickets/<email>')
def opened_tickets(email):
    user = User.query.get(email)
    tickets = Ticket.query.filter_by(email=email, status='Opened').all()
    return render_template('opened1.html', name=user.name, email=email, tickets=tickets)

@app.route('/closed_tickets/<email>')
def closed_tickets(email):
    user = User.query.get(email)
    tickets = Ticket.query.filter_by(email=email, status='Closed').all()
    return render_template('closed1.html', name=user.name, email=email, tickets=tickets)

@app.route('/admin_edit_ticket/<ticket_id>', methods=['POST'])
def admin_edit_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        ticket.status = request.form['status']
        db.session.commit()
        if ticket.status == 'Closed':
            send_closure_email(ticket.email, ticket.id, ticket)
    return redirect(url_for('admin_dashboard'))

# This one is for department_tickets.html
@app.route('/mark_priority/<ticket_id>/<department>', methods=['POST'])
def mark_priority_department(ticket_id, department):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        ticket.priority = not ticket.priority
        db.session.commit()
    return redirect(url_for('view_tickets_by_department', department=department))

# This one is for admin_dashboard.html
@app.route('/mark_priority/<ticket_id>', methods=['POST'])
def mark_priority(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        ticket.priority = not ticket.priority
        db.session.commit()
    return redirect(url_for('admin_dashboard'))


@app.route('/view_opened')
def view_opened():
    tickets = Ticket.query.filter_by(status='Opened').all()
    return render_template('admin_dashboard.html', tickets=tickets)

@app.route('/view_closed')
def view_closed():
    tickets = Ticket.query.filter_by(status='Closed').all()
    return render_template('admin_dashboard.html', tickets=tickets)

@app.route('/search_tickets', methods=['GET'])
def search_tickets():
    query = request.args.get('query', '')
    tickets = Ticket.query.filter(
        db.or_(
            Ticket.name.ilike(f'%{query}%'),
            Ticket.subject.ilike(f'%{query}%')
        )
    ).all()
    return render_template('admin_dashboard.html', tickets=tickets)

@app.route('/sort_tickets', methods=['GET'])
def sort_tickets():
    order = request.args.get('order', 'latest')
    tickets = Ticket.query.all()
    try:
        sorted_tickets = sorted(
            tickets,
            key=lambda t: datetime.strptime(t.date, "%d/%m/%Y"),
            reverse=(order == 'latest')
        )
    except Exception as e:
        flash(f"Error in sorting: {e}")
        sorted_tickets = tickets
    return render_template('admin_dashboard.html', tickets=sorted_tickets)

@app.route('/departments')
def departments():
    departments = [d[0] for d in db.session.query(Ticket.department).distinct()]
    return render_template('departments.html', departments=departments)

@app.route('/view_tickets_by_department/<department>')
def view_tickets_by_department(department):
    tickets = Ticket.query.filter_by(department=department).order_by(Ticket.priority.desc()).all()
    return render_template('department_tickets.html', department=department, tickets=tickets)

# -------------------- Email Utilities --------------------

def send_email(user_email, ticket_id, ticket):
    msg = Message(f'Ticket Raised: {ticket_id}', recipients=[user_email])
    msg.body = f"""Dear {ticket.name},

Your ticket has been successfully raised.

Ticket ID: {ticket_id}
Status: {ticket.status}
Subject: {ticket.subject}
Department: {ticket.department}
Location: {ticket.location}
Room: {ticket.room}
Mobile: {ticket.mobile}
Time: {ticket.time}

Thank you,
Help Desk Team"""
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

def send_closure_email(user_email, ticket_id, ticket):
    msg = Message(f'Ticket Closed: {ticket_id}', recipients=[user_email])
    msg.body = f"""Dear {ticket.name},

Your ticket has been closed.

Ticket ID: {ticket_id}
Status: {ticket.status}
Subject: {ticket.subject}
Department: {ticket.department}
Location: {ticket.location}
Room: {ticket.room}
Mobile: {ticket.mobile}
Time: {ticket.time}

Thank you,
Help Desk Team"""
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending closure email: {e}")

# -------------------- Run App --------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
