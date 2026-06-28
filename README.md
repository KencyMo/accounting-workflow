# Accounting Workflow

A web-based accounting system with AI assistance powered by Claude. Manage invoices, track payments, and get intelligent insights about your finances.

## Features

✅ **Invoice Management** - Create and track invoices
✅ **Client Management** - Store and manage client information
✅ **Payment Tracking** - Record and track payments
✅ **Dashboard** - Real-time financial overview
✅ **Claude AI Assistant** - Ask questions about your finances in natural language
✅ **Beautiful UI** - Modern, responsive web interface

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Anthropic API key (get one at https://console.anthropic.com/)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/KencyMo/accounting-workflow.git
   cd accounting-workflow
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open in browser**
   Navigate to `http://localhost:5000`

## Usage

### Dashboard
View your financial overview at a glance:
- Total revenue
- Total paid amount
- Outstanding balance
- Number of unpaid invoices
- Total clients and invoices

### Invoices
- Create new invoices with client info, amount, and due dates
- View all invoices and their payment status
- Record payments against invoices
- Automatic status updates (unpaid → partially paid → paid)

### Clients
- Add new clients with contact information
- Store email, phone, and address details
- Manage client relationships

### Claude Assistant
Chat with Claude to:
- "Show me all unpaid invoices"
- "What's my total revenue this month?"
- "Which client owes me the most?"
- "What was my income last quarter?"
- Any other accounting-related questions

## Database

The app uses SQLite for data storage. The database file (`accounting.db`) is created automatically when you first run the application.

## API Endpoints

- `GET /api/dashboard` - Get dashboard statistics
- `GET/POST /api/clients` - List or create clients
- `GET/PUT/DELETE /api/clients/<id>` - Manage individual clients
- `GET/POST /api/invoices` - List or create invoices
- `GET/PUT/DELETE /api/invoices/<id>` - Manage individual invoices
- `POST /api/payments` - Record a payment
- `GET /api/invoices/<id>/payments` - Get payments for an invoice
- `POST /api/chat` - Chat with Claude

## Configuration

Edit `app.py` to customize:
- Database location
- Flask port
- Claude model (currently using claude-3-5-sonnet-20241022)
- UI styling

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"  
Make sure you've installed dependencies: `pip install -r requirements.txt`

### "Error: Could not connect to API"  
Check that your Anthropic API key is correctly set in the `.env` file

### Port 5000 already in use  
Edit `app.py` and change the port: `app.run(debug=True, port=5001)`

## Future Enhancements

- Export invoices to PDF
- Email invoice reminders
- Expense tracking
- Multi-user support
- Advanced financial reports
- Invoice templates
- Payment reminders and notifications

## License

MIT License - feel free to use this project for personal or commercial purposes!

## Support

For issues or questions, please create an issue on the GitHub repository.
