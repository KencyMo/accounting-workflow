from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounting.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
CORS(app)

client = Anthropic()

# Database Models
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    invoices = db.relationship('Invoice', backref='client', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'created_at': self.created_at.isoformat()
        }

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='unpaid')  # unpaid, partially_paid, paid
    amount_paid = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    payments = db.relationship('Payment', backref='invoice', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'client_id': self.client_id,
            'client_name': self.client.name if self.client else 'Unknown',
            'amount': self.amount,
            'description': self.description,
            'status': self.status,
            'amount_paid': self.amount_paid,
            'amount_remaining': self.amount - self.amount_paid,
            'created_at': self.created_at.isoformat(),
            'due_date': self.due_date.isoformat() if self.due_date else None
        }

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))  # cash, check, credit_card, bank_transfer
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat(),
            'payment_method': self.payment_method,
            'notes': self.notes
        }

# Routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/clients', methods=['GET', 'POST'])
def clients():
    if request.method == 'POST':
        data = request.json
        client = Client(
            name=data['name'],
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_dict()), 201
    
    clients_list = Client.query.all()
    return jsonify([c.to_dict() for c in clients_list])

@app.route('/api/clients/<int:client_id>', methods=['GET', 'PUT', 'DELETE'])
def client_detail(client_id):
    client = Client.query.get_or_404(client_id)
    
    if request.method == 'GET':
        return jsonify(client.to_dict())
    elif request.method == 'PUT':
        data = request.json
        client.name = data.get('name', client.name)
        client.email = data.get('email', client.email)
        client.phone = data.get('phone', client.phone)
        client.address = data.get('address', client.address)
        db.session.commit()
        return jsonify(client.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(client)
        db.session.commit()
        return '', 204

@app.route('/api/invoices', methods=['GET', 'POST'])
def invoices():
    if request.method == 'POST':
        data = request.json
        invoice = Invoice(
            invoice_number=data['invoice_number'],
            client_id=data['client_id'],
            amount=data['amount'],
            description=data.get('description'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        )
        db.session.add(invoice)
        db.session.commit()
        return jsonify(invoice.to_dict()), 201
    
    invoices_list = Invoice.query.all()
    return jsonify([i.to_dict() for i in invoices_list])

@app.route('/api/invoices/<int:invoice_id>', methods=['GET', 'PUT', 'DELETE'])
def invoice_detail(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    
    if request.method == 'GET':
        return jsonify(invoice.to_dict())
    elif request.method == 'PUT':
        data = request.json
        invoice.amount = data.get('amount', invoice.amount)
        invoice.description = data.get('description', invoice.description)
        invoice.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else invoice.due_date
        db.session.commit()
        return jsonify(invoice.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(invoice)
        db.session.commit()
        return '', 204

@app.route('/api/payments', methods=['POST'])
def create_payment():
    data = request.json
    invoice = Invoice.query.get_or_404(data['invoice_id'])
    
    payment = Payment(
        invoice_id=data['invoice_id'],
        amount=data['amount'],
        payment_method=data.get('payment_method'),
        notes=data.get('notes')
    )
    
    invoice.amount_paid += data['amount']
    
    # Update invoice status
    if invoice.amount_paid >= invoice.amount:
        invoice.status = 'paid'
    elif invoice.amount_paid > 0:
        invoice.status = 'partially_paid'
    else:
        invoice.status = 'unpaid'
    
    db.session.add(payment)
    db.session.commit()
    
    return jsonify(payment.to_dict()), 201

@app.route('/api/invoices/<int:invoice_id>/payments', methods=['GET'])
def invoice_payments(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    payments = Payment.query.filter_by(invoice_id=invoice_id).all()
    return jsonify([p.to_dict() for p in payments])

@app.route('/api/dashboard')
def dashboard():
    invoices_list = Invoice.query.all()
    total_revenue = sum(i.amount for i in invoices_list)
    total_paid = sum(i.amount_paid for i in invoices_list)
    total_unpaid = total_revenue - total_paid
    unpaid_invoices = len([i for i in invoices_list if i.status in ['unpaid', 'partially_paid']])
    
    return jsonify({
        'total_revenue': total_revenue,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'unpaid_invoices': unpaid_invoices,
        'total_clients': Client.query.count(),
        'total_invoices': len(invoices_list)
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    
    # Get context from database
    invoices_list = Invoice.query.all()
    clients_list = Client.query.all()
    
    context = f"""
    You are an accounting assistant. You have access to the following data:
    
    Invoices:
    {json.dumps([i.to_dict() for i in invoices_list], indent=2)}
    
    Clients:
    {json.dumps([c.to_dict() for c in clients_list], indent=2)}
    
    Help the user with their accounting queries and provide insights based on this data.
    """
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=context,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        response = message.content[0].text
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
