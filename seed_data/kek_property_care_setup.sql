-- KEK Property Care LLC - Chart of Accounts & Seed Data
-- Fiscal Year: Jan-Dec (2024)
-- Structure: LLC, Per-job/Subscription revenue, 2 operators, FL (No Sales Tax)

-- ============================================
-- CHART OF ACCOUNTS
-- ============================================

-- ASSETS (1000-1999)
INSERT INTO chart_of_accounts (account_number, account_name, account_type, description) VALUES
('1000', 'Cash - Operating', 'ASSET', 'Main business checking account'),
('1010', 'Cash - Payroll', 'ASSET', 'Payroll reserve account'),
('1050', 'Petty Cash', 'ASSET', 'Small daily cash expenses'),
('1200', 'Accounts Receivable', 'ASSET', 'Unpaid customer invoices'),
('1500', 'Equipment & Tools', 'ASSET', 'Cleaning equipment, vacuum, supplies cart'),
('1510', 'Accumulated Depreciation - Equipment', 'ASSET', 'Depreciation contra-account'),
('1600', 'Vehicle', 'ASSET', 'Service vehicle'),
('1610', 'Accumulated Depreciation - Vehicle', 'ASSET', 'Vehicle depreciation'),
('1700', 'Supplies Inventory', 'ASSET', 'Cleaning chemicals, microfiber cloths, etc');

-- LIABILITIES (2000-2999)
INSERT INTO chart_of_accounts (account_number, account_name, account_type, description) VALUES
('2000', 'Accounts Payable', 'LIABILITY', 'Owed to suppliers'),
('2100', 'Sales Tax Payable', 'LIABILITY', 'Sales tax collected (N/A for FL)'),
('2200', 'Payroll Taxes Payable', 'LIABILITY', 'FICA, unemployment taxes'),
('2500', 'Equipment Loan', 'LIABILITY', 'Financed cleaning equipment');

-- EQUITY (3000-3999)
INSERT INTO chart_of_accounts (account_number, account_name, account_type, description) VALUES
('3000', 'Owner Capital - You', 'EQUITY', 'Your capital contribution'),
('3010', 'Owner Capital - Mom', 'EQUITY', 'Mom''s capital contribution'),
('3100', 'Owner Draw - You', 'EQUITY', 'Your draws/distributions'),
('3110', 'Owner Draw - Mom', 'EQUITY', 'Mom''s draws/distributions'),
('3500', 'Retained Earnings', 'EQUITY', 'Prior year net income');

-- REVENUE (4000-4999)
INSERT INTO chart_of_accounts (account_number, account_name, account_type, description) VALUES
('4000', 'Residential Cleaning Revenue', 'REVENUE', 'Per-job residential cleaning'),
('4010', 'Residential Subscription Revenue', 'REVENUE', 'Monthly recurring residential'),
('4100', 'Commercial Cleaning Revenue', 'REVENUE', 'Per-job commercial cleaning'),
('4110', 'Commercial Subscription Revenue', 'REVENUE', 'Monthly recurring commercial'),
('4200', 'Post-Construction Cleaning', 'REVENUE', 'New construction/renovation cleanup'),
('4300', 'Carpet Cleaning Revenue', 'REVENUE', 'Specialized carpet cleaning service'),
('4900', 'Other Income', 'REVENUE', 'Miscellaneous revenue');

-- EXPENSES (5000-5999)
INSERT INTO chart_of_accounts (account_number, account_name, account_type, description) VALUES
('5000', 'Cleaning Supplies', 'EXPENSE', 'Chemicals, cloths, paper products'),
('5010', 'Equipment Maintenance', 'EXPENSE', 'Repair and maintenance of equipment'),
('5020', 'Equipment Replacement', 'EXPENSE', 'Small tools under $2,500'),
('5100', 'Vehicle Expenses - Gas', 'EXPENSE', 'Fuel for service vehicle'),
('5110', 'Vehicle Expenses - Maintenance', 'EXPENSE', 'Oil changes, repairs, tires'),
('5120', 'Vehicle Expenses - Insurance', 'EXPENSE', 'Vehicle insurance premium'),
('5130', 'Vehicle Expenses - Registration', 'EXPENSE', 'License plate, registration'),
('5200', 'Mileage - Work Related', 'EXPENSE', 'Mileage deduction tracking'),
('5300', 'Payroll - Operator Wages', 'EXPENSE', 'Your wages (if taking salary)'),
('5310', 'Payroll - Mom Wages', 'EXPENSE', 'Mom''s wages if she takes salary'),
('5400', 'Payroll Taxes - FICA', 'EXPENSE', 'Social Security & Medicare'),
('5410', 'Payroll Taxes - Unemployment', 'EXPENSE', 'Federal & State unemployment'),
('5420', 'Payroll Taxes - Workers Comp', 'EXPENSE', 'Workers'' compensation insurance'),
('5500', 'Business Insurance - Liability', 'EXPENSE', 'General liability insurance'),
('5510', 'Business Insurance - Property', 'EXPENSE', 'Equipment/property insurance'),
('5600', 'Office/Storage Space', 'EXPENSE', 'Rent for office or storage'),
('5700', 'Utilities - Internet', 'EXPENSE', 'Internet for business'),
('5710', 'Utilities - Phone', 'EXPENSE', 'Cell phone for business'),
('5800', 'Marketing & Advertising', 'EXPENSE', 'Website, flyers, ads, Nextdoor, Google'),
('5900', 'Professional Services - Accounting', 'EXPENSE', 'Bookkeeper/accountant fees'),
('5910', 'Professional Services - Legal', 'EXPENSE', 'Attorney, business formation'),
('6000', 'Depreciation - Equipment', 'EXPENSE', 'Annual depreciation'),
('6010', 'Depreciation - Vehicle', 'EXPENSE', 'Annual vehicle depreciation'),
('6100', 'Bank Fees', 'EXPENSE', 'Monthly bank service charges'),
('6200', 'Software Subscriptions', 'EXPENSE', 'Accounting, scheduling, management apps');

-- ============================================
-- OPENING BALANCES (Jan 1, 2024)
-- ============================================

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-01', 'JE-001', 'Opening Entry - KEK Property Care LLC Formation', 'Initial capital contribution and equipment purchase');

-- Your capital contribution: $10,000
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash from owner capital', 10000.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '3000', 'Owner capital - You', NULL, 10000.00);

-- Mom's capital contribution: $5,000
INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-01', 'JE-002', 'Capital contribution from Mom', 'Mom''s initial investment');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash from mom capital', 5000.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '3010', 'Owner capital - Mom', NULL, 5000.00);

-- Equipment purchase: $4,500 (vacuum, supplies, cart)
INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-02', 'JE-003', 'Purchase equipment and supplies', 'Industrial vacuum, supplies cart, initial inventory');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1500', 'Equipment purchase', 3000.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1700', 'Supplies inventory', 1500.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash paid for equipment', NULL, 4500.00);

-- Vehicle purchase: $12,000 (used van)
INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-03', 'JE-004', 'Purchase service vehicle', 'Used cleaning van');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1600', 'Vehicle purchase', 12000.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '2500', 'Equipment loan', NULL, 12000.00);

-- ============================================
-- SAMPLE CLIENTS
-- ============================================

INSERT INTO clients (name, email, phone, address, client_type, monthly_contract) VALUES
('The Martinez Family', 'martinez@email.com', '(305) 555-0101', '2847 Oak Street, Miami, FL 33125', 'Residential', TRUE),
('Downtown Medical Complex', 'facilities@downtown-medical.com', '(305) 555-0202', '1200 Biscayne Blvd, Miami, FL 33132', 'Commercial', TRUE),
('Johnson Family Residence', 'johnson@email.com', '(305) 555-0303', '5921 Coral Avenue, Coral Gables, FL 33146', 'Residential', FALSE),
('Tech Startup Hub - Miami', 'admin@techstartup.com', '(305) 555-0404', '900 Brickell Ave, Miami, FL 33131', 'Commercial', TRUE),
('Rivera Home Services', 'rivera@email.com', '(305) 555-0505', '3456 Tamiami Trail, Miami, FL 33144', 'Residential', TRUE),
('Beachfront Office Park', 'management@beachfront.com', '(305) 555-0606', '2000 Ocean Drive, Miami Beach, FL 33139', 'Commercial', FALSE);

-- ============================================
-- SAMPLE INVOICES (Jan-Mar 2024)
-- ============================================

-- January Invoices
INSERT INTO invoices (invoice_number, client_id, invoice_date, due_date, description, amount, status, amount_paid) VALUES
('INV-2024-001', 1, '2024-01-05', '2024-01-20', 'Monthly Residential Cleaning - January', 300.00, 'paid', 300.00),
('INV-2024-002', 2, '2024-01-05', '2024-01-20', 'Monthly Commercial Cleaning - January', 1200.00, 'paid', 1200.00),
('INV-2024-003', 3, '2024-01-08', '2024-01-25', 'Post-Construction Deep Clean - Johnson Residence', 650.00, 'paid', 650.00),
('INV-2024-004', 4, '2024-01-10', '2024-01-25', 'Monthly Commercial Cleaning - January', 1500.00, 'paid', 1500.00),
('INV-2024-005', 5, '2024-01-15', '2024-01-30', 'Monthly Residential Cleaning - January', 300.00, 'paid', 300.00),
('INV-2024-006', 6, '2024-01-20', '2024-02-05', 'Carpet Cleaning - Beachfront Office Park', 800.00, 'paid', 800.00);

-- February Invoices
INSERT INTO invoices (invoice_number, client_id, invoice_date, due_date, description, amount, status, amount_paid) VALUES
('INV-2024-007', 1, '2024-02-05', '2024-02-20', 'Monthly Residential Cleaning - February', 300.00, 'paid', 300.00),
('INV-2024-008', 2, '2024-02-05', '2024-02-20', 'Monthly Commercial Cleaning - February', 1200.00, 'paid', 1200.00),
('INV-2024-009', 3, '2024-02-12', '2024-02-28', 'Window Cleaning - Johnson Residence', 250.00, 'paid', 250.00),
('INV-2024-010', 4, '2024-02-10', '2024-02-25', 'Monthly Commercial Cleaning - February', 1500.00, 'paid', 1500.00),
('INV-2024-011', 5, '2024-02-15', '2024-02-28', 'Monthly Residential Cleaning - February', 300.00, 'paid', 300.00),
('INV-2024-012', 2, '2024-02-20', '2024-03-06', 'Additional Office Deep Clean', 400.00, 'paid', 400.00);

-- March Invoices
INSERT INTO invoices (invoice_number, client_id, invoice_date, due_date, description, amount, status, amount_paid) VALUES
('INV-2024-013', 1, '2024-03-05', '2024-03-20', 'Monthly Residential Cleaning - March', 300.00, 'paid', 300.00),
('INV-2024-014', 2, '2024-03-05', '2024-03-20', 'Monthly Commercial Cleaning - March', 1200.00, 'paid', 1200.00),
('INV-2024-015', 4, '2024-03-10', '2024-03-25', 'Monthly Commercial Cleaning - March', 1500.00, 'unpaid', 0.00),
('INV-2024-016', 5, '2024-03-15', '2024-03-30', 'Monthly Residential Cleaning - March', 300.00, 'paid', 300.00);

-- ============================================
-- SAMPLE PAYMENTS (Jan-Mar 2024)
-- ============================================

INSERT INTO payments (invoice_id, payment_date, amount, payment_method, notes) VALUES
(1, '2024-01-15', 300.00, 'bank_transfer', 'Recurring client payment'),
(2, '2024-01-18', 1200.00, 'bank_transfer', 'Monthly commercial cleaning'),
(3, '2024-01-25', 650.00, 'check', 'Post-construction cleanup'),
(4, '2024-01-22', 1500.00, 'bank_transfer', 'Monthly commercial cleaning'),
(5, '2024-01-28', 300.00, 'cash', 'Cash payment received'),
(6, '2024-02-02', 800.00, 'bank_transfer', 'Carpet cleaning service'),
(7, '2024-02-18', 300.00, 'bank_transfer', 'Monthly subscription'),
(8, '2024-02-20', 1200.00, 'bank_transfer', 'Monthly commercial cleaning'),
(9, '2024-02-26', 250.00, 'check', 'Window cleaning service'),
(10, '2024-02-25', 1500.00, 'bank_transfer', 'Monthly commercial cleaning'),
(11, '2024-02-28', 300.00, 'cash', 'Monthly subscription payment'),
(12, '2024-03-05', 400.00, 'bank_transfer', 'Deep clean service'),
(13, '2024-03-18', 300.00, 'bank_transfer', 'Monthly subscription'),
(14, '2024-03-20', 1200.00, 'bank_transfer', 'Monthly commercial cleaning'),
(16, '2024-03-28', 300.00, 'cash', 'Monthly subscription payment');

-- ============================================
-- EXPENSE ENTRIES (Jan-Mar 2024)
-- ============================================

-- January Expenses
INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-10', 'JE-005', 'Purchase cleaning supplies', 'Bulk supply order from Sysco');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5000', 'Cleaning supplies - January', 250.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 250.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-12', 'JE-006', 'Vehicle fuel - January', 'Gas for van');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5100', 'Gas - January', 120.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 120.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-01-25', 'JE-007', 'Business liability insurance', 'Monthly premium');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5500', 'Liability insurance - January', 150.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 150.00);

-- February Expenses
INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-02-08', 'JE-008', 'Purchase cleaning supplies', 'Monthly supply order');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5000', 'Cleaning supplies - February', 280.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 280.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-02-14', 'JE-009', 'Vehicle fuel - February', 'Gas for van');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5100', 'Gas - February', 135.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 135.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-02-20', 'JE-010', 'Vehicle maintenance', 'Oil change and filter');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5110', 'Vehicle maintenance - February', 75.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 75.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-02-25', 'JE-011', 'Business liability insurance', 'Monthly premium');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5500', 'Liability insurance - February', 150.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 150.00);

-- March Expenses
INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-03-06', 'JE-012', 'Purchase cleaning supplies', 'Monthly supply order');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5000', 'Cleaning supplies - March', 300.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 300.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-03-12', 'JE-013', 'Vehicle fuel - March', 'Gas for van');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5100', 'Gas - March', 140.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 140.00);

INSERT INTO journal_entries (entry_date, entry_number, description, memo) VALUES
('2024-03-25', 'JE-014', 'Business liability insurance', 'Monthly premium');
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '5500', 'Liability insurance - March', 150.00, NULL);
INSERT INTO journal_entry_lines (entry_id, account_number, description, debit, credit) VALUES
(LAST_INSERT_ID(), '1000', 'Cash payment', NULL, 150.00);

-- ============================================
-- END OF SEED DATA
-- ============================================
