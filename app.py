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
class ChartOfAccounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_name = db.Column(db.String(120), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    description = db.Column(db.Text)
    balance = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    journal_entries = db.relationship('JournalEntry', backref='account', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'account_number': self.account_number,
            'account_name': self.account_name,
            'account_type': self.account_type,
            'description': self.description,
            'balance': self.balance,
            'created_at': self.created_at.isoformat()
        }

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_number = db.Column(db.String(50), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.id'), nullable=False)
    debit = db.Column(db.Float, default=0)
    credit = db.Column(db.Float, default=0)
    description = db.Column(db.Text)
    reference = db.Column(db.String(100))  # Reference to invoice or transaction
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'entry_number': self.entry_number,
            'account_id': self.account_id,
            'account_number': self.account.account_number if self.account else 'Unknown',
            'account_name': self.account.account_name if self.account else 'Unknown',
            'debit': self.debit,
            'credit': self.credit,
            'description': self.description,
            'reference': self.reference,
            'created_at': self.created_at.isoformat()
        }

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

# Chart of Accounts Routes
@app.route('/api/accounts', methods=['GET', 'POST'])
def accounts():
    if request.method == 'POST':
        data = request.json
        account = ChartOfAccounts(
            account_number=data['account_number'],
            account_name=data['account_name'],
            account_type=data['account_type'],
            description=data.get('description')
        )
        db.session.add(account)
        db.session.commit()
        return jsonify(account.to_dict()), 201
    
    accounts_list = ChartOfAccounts.query.all()
    return jsonify([a.to_dict() for a in accounts_list])

@app.route('/api/accounts/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
def account_detail(account_id):
    account = ChartOfAccounts.query.get_or_404(account_id)
    
    if request.method == 'GET':
        return jsonify(account.to_dict())
    elif request.method == 'PUT':
        data = request.json
        account.account_name = data.get('account_name', account.account_name)
        account.description = data.get('description', account.description)
        db.session.commit()
        return jsonify(account.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(account)
        db.session.commit()
        return '', 204

# Journal Entry Routes
@app.route('/api/journal-entries', methods=['GET', 'POST'])
def journal_entries():
    if request.method == 'POST':
        data = request.json
        account = ChartOfAccounts.query.get_or_404(data['account_id'])
        
        # Generate entry number
        last_entry = JournalEntry.query.order_by(JournalEntry.id.desc()).first()
        entry_number = f"JE{str(last_entry.id + 1 if last_entry else 1).zfill(6)}"
        
        entry = JournalEntry(
            entry_number=entry_number,
            account_id=data['account_id'],
            debit=data.get('debit', 0),
            credit=data.get('credit', 0),
            description=data.get('description'),
            reference=data.get('reference')
        )
        
        # Update account balance
        if entry.debit > 0:
            account.balance += entry.debit
        if entry.credit > 0:
            account.balance -= entry.credit
        
        db.session.add(entry)
        db.session.commit()
        return jsonify(entry.to_dict()), 201
    
    entries_list = JournalEntry.query.all()
    return jsonify([e.to_dict() for e in entries_list])

@app.route('/api/journal-entries/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
def journal_entry_detail(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    
    if request.method == 'GET':
        return jsonify(entry.to_dict())
    elif request.method == 'PUT':
        data = request.json
        old_debit = entry.debit
        old_credit = entry.credit
        
        entry.debit = data.get('debit', entry.debit)
        entry.credit = data.get('credit', entry.credit)
        entry.description = data.get('description', entry.description)
        
        # Adjust account balance
        account = entry.account
        account.balance -= old_debit
        account.balance += old_credit
        account.balance += entry.debit
        account.balance -= entry.credit
        
        db.session.commit()
        return jsonify(entry.to_dict())
    elif request.method == 'DELETE':
        account = entry.account
        account.balance -= entry.debit
        account.balance += entry.credit
        db.session.delete(entry)
        db.session.commit()
        return '', 204

@app.route('/api/accounts/<int:account_id>/journal-entries', methods=['GET'])
def account_journal_entries(account_id):
    entries = JournalEntry.query.filter_by(account_id=account_id).all()
    return jsonify([e.to_dict() for e in entries])

# Trial Balance Route
@app.route('/api/trial-balance')
def trial_balance():
    accounts_list = ChartOfAccounts.query.all()
    trial_balance_data = []
    total_debits = 0
    total_credits = 0
    
    for account in accounts_list:
        account_data = account.to_dict()
        
        # Asset, Expense accounts increase with debit
        # Liability, Equity, Revenue accounts increase with credit
        if account.account_type in ['Asset', 'Expense']:
            account_data['debit'] = max(0, account.balance)
            account_data['credit'] = max(0, -account.balance)
        else:  # Liability, Equity, Revenue
            account_data['debit'] = max(0, -account.balance)
            account_data['credit'] = max(0, account.balance)
        
        total_debits += account_data['debit']
        total_credits += account_data['credit']
        trial_balance_data.append(account_data)
    
    return jsonify({
        'accounts': trial_balance_data,
        'total_debits': total_debits,
        'total_credits': total_credits,
        'is_balanced': abs(total_debits - total_credits) < 0.01
    })

# General Ledger Route
@app.route('/api/general-ledger')
def general_ledger():
    accounts_list = ChartOfAccounts.query.all()
    ledger = []
    
    for account in accounts_list:
        account_data = account.to_dict()
        account_data['entries'] = [e.to_dict() for e in account.journal_entries]
        ledger.append(account_data)
    
    return jsonify(ledger)

# Income Statement Route
@app.route('/api/income-statement')
def income_statement():
    accounts_list = ChartOfAccounts.query.all()
    
    total_revenue = sum(a.balance for a in accounts_list if a.account_type == 'Revenue')
    total_expenses = sum(a.balance for a in accounts_list if a.account_type == 'Expense')
    net_income = total_revenue - total_expenses
    
    revenue_accounts = [a.to_dict() for a in accounts_list if a.account_type == 'Revenue']
    expense_accounts = [a.to_dict() for a in accounts_list if a.account_type == 'Expense']
    
    return jsonify({
        'revenue_accounts': revenue_accounts,
        'expense_accounts': expense_accounts,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_income': net_income
    })

# Balance Sheet Route
@app.route('/api/balance-sheet')
def balance_sheet():
    accounts_list = ChartOfAccounts.query.all()
    
    assets = [a.to_dict() for a in accounts_list if a.account_type == 'Asset']
    liabilities = [a.to_dict() for a in accounts_list if a.account_type == 'Liability']
    equity = [a.to_dict() for a in accounts_list if a.account_type == 'Equity']
    
    total_assets = sum(a['balance'] for a in assets)
    total_liabilities = sum(a['balance'] for a in liabilities)
    total_equity = sum(a['balance'] for a in equity)
    
    return jsonify({
        'assets': assets,
        'liabilities': liabilities,
        'equity': equity,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'total_equity': total_equity,
        'is_balanced': abs((total_liabilities + total_equity) - total_assets) < 0.01
    })

# Client Routes
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

# Invoice Routes
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

# Payment Routes
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

# Dashboard Route
@app.route('/api/dashboard')
def dashboard():
    invoices_list = Invoice.query.all()
    total_revenue = sum(i.amount for i in invoices_list)
    total_paid = sum(i.amount_paid for i in invoices_list)
    total_unpaid = total_revenue - total_paid
    unpaid_invoices = len([i for i in invoices_list if i.status in ['unpaid', 'partially_paid']])
    
    accounts_list = ChartOfAccounts.query.all()
    total_assets = sum(a.balance for a in accounts_list if a.account_type == 'Asset')
    total_liabilities = sum(a.balance for a in accounts_list if a.account_type == 'Liability')
    
    return jsonify({
        'total_revenue': total_revenue,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'unpaid_invoices': unpaid_invoices,
        'total_clients': Client.query.count(),
        'total_invoices': len(invoices_list),
        'total_accounts': len(accounts_list),
        'total_assets': total_assets,
        'total_liabilities': total_liabilities
    })

# Chat Route
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Message required'}), 400
    
    # Get context from database
    invoices_list = Invoice.query.all()
    clients_list = Client.query.all()
    accounts_list = ChartOfAccounts.query.all()
    entries_list = JournalEntry.query.all()
    
    context = f"""
    You are an accounting assistant. You have access to the following data:
    
    Chart of Accounts:
    {json.dumps([a.to_dict() for a in accounts_list], indent=2)}
    
    Journal Entries:
    {json.dumps([e.to_dict() for e in entries_list], indent=2)}
    
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
