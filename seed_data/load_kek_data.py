"""
KEK Property Care LLC - SQLite Data Loader
Imports seed data into the Flask accounting app database
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DATABASE_PATH = "instance/accounting.db"

def load_kek_property_care_data():
    """Load complete KEK Property Care accounting data"""
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    print("📊 Loading KEK Property Care LLC Data...")
    print("=" * 60)
    
    # ============================================
    # CREATE CLIENTS
    # ============================================
    print("\n✓ Creating clients...")
    
    clients = [
        ("The Martinez Family", "martinez@email.com", "(305) 555-0101", 
         "2847 Oak Street, Miami, FL 33125", "Residential", True),
        ("Downtown Medical Complex", "facilities@downtown-medical.com", "(305) 555-0202", 
         "1200 Biscayne Blvd, Miami, FL 33132", "Commercial", True),
        ("Johnson Family Residence", "johnson@email.com", "(305) 555-0303", 
         "5921 Coral Avenue, Coral Gables, FL 33146", "Residential", False),
        ("Tech Startup Hub - Miami", "admin@techstartup.com", "(305) 555-0404", 
         "900 Brickell Ave, Miami, FL 33131", "Commercial", True),
        ("Rivera Home Services", "rivera@email.com", "(305) 555-0505", 
         "3456 Tamiami Trail, Miami, FL 33144", "Residential", True),
        ("Beachfront Office Park", "management@beachfront.com", "(305) 555-0606", 
         "2000 Ocean Drive, Miami Beach, FL 33139", "Commercial", False),
    ]
    
    for name, email, phone, address, client_type, contract in clients:
        cursor.execute("""
            INSERT INTO client (name, email, phone, address, client_type, monthly_contract)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, phone, address, client_type, contract))
    
    conn.commit()
    client_ids = [row[0] for row in cursor.execute("SELECT id FROM client ORDER BY id").fetchall()]
    print(f"   Created {len(client_ids)} clients")
    
    # ============================================
    # CREATE INVOICES - JANUARY
    # ============================================
    print("\n✓ Creating January invoices...")
    
    jan_invoices = [
        (1, "2024-01-05", "2024-01-20", "Monthly Residential Cleaning - January", 300.00, "paid"),
        (2, "2024-01-05", "2024-01-20", "Monthly Commercial Cleaning - January", 1200.00, "paid"),
        (3, "2024-01-08", "2024-01-25", "Post-Construction Deep Clean - Johnson Residence", 650.00, "paid"),
        (4, "2024-01-10", "2024-01-25", "Monthly Commercial Cleaning - January", 1500.00, "paid"),
        (5, "2024-01-15", "2024-01-30", "Monthly Residential Cleaning - January", 300.00, "paid"),
        (6, "2024-01-20", "2024-02-05", "Carpet Cleaning - Beachfront Office Park", 800.00, "paid"),
    ]
    
    invoice_counter = 1
    invoice_ids = {}
    
    for idx, (client_id, inv_date, due_date, description, amount, status) in enumerate(jan_invoices, 1):
        invoice_num = f"INV-2024-{invoice_counter:03d}"
        cursor.execute("""
            INSERT INTO invoice 
            (invoice_number, client_id, invoice_date, due_date, description, amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (invoice_num, client_id, inv_date, due_date, description, amount, status))
        
        inv_id = cursor.lastrowid
        invoice_ids[invoice_counter] = inv_id
        invoice_counter += 1
    
    conn.commit()
    print(f"   Created 6 invoices for January")
    
    # ============================================
    # CREATE INVOICES - FEBRUARY
    # ============================================
    print("✓ Creating February invoices...")
    
    feb_invoices = [
        (1, "2024-02-05", "2024-02-20", "Monthly Residential Cleaning - February", 300.00, "paid"),
        (2, "2024-02-05", "2024-02-20", "Monthly Commercial Cleaning - February", 1200.00, "paid"),
        (3, "2024-02-12", "2024-02-28", "Window Cleaning - Johnson Residence", 250.00, "paid"),
        (4, "2024-02-10", "2024-02-25", "Monthly Commercial Cleaning - February", 1500.00, "paid"),
        (5, "2024-02-15", "2024-02-28", "Monthly Residential Cleaning - February", 300.00, "paid"),
        (2, "2024-02-20", "2024-03-06", "Additional Office Deep Clean", 400.00, "paid"),
    ]
    
    for idx, (client_id, inv_date, due_date, description, amount, status) in enumerate(feb_invoices, 1):
        invoice_num = f"INV-2024-{invoice_counter:03d}"
        cursor.execute("""
            INSERT INTO invoice 
            (invoice_number, client_id, invoice_date, due_date, description, amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (invoice_num, client_id, inv_date, due_date, description, amount, status))
        
        inv_id = cursor.lastrowid
        invoice_ids[invoice_counter] = inv_id
        invoice_counter += 1
    
    conn.commit()
    print(f"   Created 6 invoices for February")
    
    # ============================================
    # CREATE INVOICES - MARCH
    # ============================================
    print("✓ Creating March invoices...")
    
    mar_invoices = [
        (1, "2024-03-05", "2024-03-20", "Monthly Residential Cleaning - March", 300.00, "paid"),
        (2, "2024-03-05", "2024-03-20", "Monthly Commercial Cleaning - March", 1200.00, "paid"),
        (4, "2024-03-10", "2024-03-25", "Monthly Commercial Cleaning - March", 1500.00, "unpaid"),
        (5, "2024-03-15", "2024-03-30", "Monthly Residential Cleaning - March", 300.00, "paid"),
    ]
    
    for idx, (client_id, inv_date, due_date, description, amount, status) in enumerate(mar_invoices, 1):
        invoice_num = f"INV-2024-{invoice_counter:03d}"
        cursor.execute("""
            INSERT INTO invoice 
            (invoice_number, client_id, invoice_date, due_date, description, amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (invoice_num, client_id, inv_date, due_date, description, amount, status))
        
        inv_id = cursor.lastrowid
        invoice_ids[invoice_counter] = inv_id
        invoice_counter += 1
    
    conn.commit()
    print(f"   Created 4 invoices for March")
    
    # ============================================
    # CREATE PAYMENTS
    # ============================================
    print("\n✓ Creating payments...")
    
    payments = [
        (1, "2024-01-15", 300.00, "bank_transfer"),
        (2, "2024-01-18", 1200.00, "bank_transfer"),
        (3, "2024-01-25", 650.00, "check"),
        (4, "2024-01-22", 1500.00, "bank_transfer"),
        (5, "2024-01-28", 300.00, "cash"),
        (6, "2024-02-02", 800.00, "bank_transfer"),
        (7, "2024-02-18", 300.00, "bank_transfer"),
        (8, "2024-02-20", 1200.00, "bank_transfer"),
        (9, "2024-02-26", 250.00, "check"),
        (10, "2024-02-25", 1500.00, "bank_transfer"),
        (11, "2024-02-28", 300.00, "cash"),
        (12, "2024-03-05", 400.00, "bank_transfer"),
        (13, "2024-03-18", 300.00, "bank_transfer"),
        (14, "2024-03-20", 1200.00, "bank_transfer"),
        (16, "2024-03-28", 300.00, "cash"),
    ]
    
    for invoice_num, pay_date, amount, method in payments:
        if invoice_num in invoice_ids:
            invoice_id = invoice_ids[invoice_num]
            cursor.execute("""
                INSERT INTO payment (invoice_id, payment_date, amount, payment_method)
                VALUES (?, ?, ?, ?)
            """, (invoice_id, pay_date, amount, method))
    
    conn.commit()
    print(f"   Created 15 payments")
    
    # ============================================
    # SUMMARY STATISTICS
    # ============================================
    print("\n" + "=" * 60)
    print("📈 Q1 2024 KEK PROPERTY CARE SUMMARY")
    print("=" * 60)
    
    # Total revenue
    total_revenue = cursor.execute(
        "SELECT SUM(amount) FROM invoice WHERE status = 'paid'"
    ).fetchone()[0] or 0
    print(f"\n💰 Total Revenue (Paid):        ${total_revenue:,.2f}")
    
    # Unpaid
    unpaid = cursor.execute(
        "SELECT SUM(amount) FROM invoice WHERE status = 'unpaid'"
    ).fetchone()[0] or 0
    print(f"⏳ Unpaid Outstanding:         ${unpaid:,.2f}")
    
    # Total invoices
    total_invoices = cursor.execute(
        "SELECT COUNT(*) FROM invoice"
    ).fetchone()[0]
    print(f"📄 Total Invoices:             {total_invoices}")
    
    # By client type
    residential = cursor.execute(
        "SELECT SUM(i.amount) FROM invoice i JOIN client c ON i.client_id = c.id WHERE c.client_type = 'Residential' AND i.status = 'paid'"
    ).fetchone()[0] or 0
    
    commercial = cursor.execute(
        "SELECT SUM(i.amount) FROM invoice i JOIN client c ON i.client_id = c.id WHERE c.client_type = 'Commercial' AND i.status = 'paid'"
    ).fetchone()[0] or 0
    
    print(f"\n   Residential Revenue:        ${residential:,.2f}")
    print(f"   Commercial Revenue:        ${commercial:,.2f}")
    
    # Revenue breakdown by type
    print(f"\n📊 Revenue Breakdown:")
    cursor.execute("""
        SELECT description, SUM(amount) as total
        FROM invoice
        WHERE status = 'paid'
        GROUP BY description
        ORDER BY total DESC
    """)
    
    for desc, total in cursor.fetchall():
        print(f"   • {desc[:40]:<40} ${total:>8,.2f}")
    
    print("\n" + "=" * 60)
    print("✅ Data load complete!")
    print("=" * 60)
    
    conn.close()


if __name__ == "__main__":
    try:
        load_kek_property_care_data()
    except Exception as e:
        print(f"\n❌ Error loading data: {e}")
        import traceback
        traceback.print_exc()
