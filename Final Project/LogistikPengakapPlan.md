# Project Plan: LogistikPengakap

## 1. Overview & Real-World Problem
Local scout troops (*Kumpulan Pengakap*) manage sizeable inventories of shared equipment—including camping tents, pioneering ropes, cooking sets, spars, and lanterns. Gear loans before campouts are typically tracked using paper sign-out sheets or whiteboards. Equipment frequently goes missing, gets damaged without being reported, or remains unreturned, placing a heavy financial burden on troop funds to replace lost gear.

**LogistikPengakap** is a dedicated equipment inventory and loan management system tailored for troop Quartermasters (*Kuartermastik*).

---

## 2. Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js (TypeScript), Tailwind CSS | Gear catalog view, loan checkout interface, return verification UI |
| **Backend** | Python (FastAPI / Django REST Framework) | Automated overdue tracking, maintenance alerts, inventory status logic |
| **Database** | PostgreSQL | Relational schema for items, categories, loans, and damage reports |
| **Auth** | JWT (JSON Web Tokens) | Quartermasters (*Admin*) vs. Troop Members (*Scout/Leader*) |

---

## 3. Database Schema

```sql
-- Equipment Category Table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL -- e.g., Tents, Ropes, Cooking, Pioneering
);

-- Equipment Inventory Table
CREATE TABLE inventory_items (
    id SERIAL PRIMARY KEY,
    item_code VARCHAR(30) UNIQUE NOT NULL, -- e.g., TNT-001
    name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    condition VARCHAR(20) DEFAULT 'Good' CHECK (condition IN ('Good', 'Fair', 'Needs Repair', 'Damaged', 'Lost')),
    status VARCHAR(20) DEFAULT 'Available' CHECK (status IN ('Available', 'Loaned', 'Maintenance', 'Retired')),
    storage_location VARCHAR(50) NOT NULL, -- e.g., Store Room Rack B
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users / Borrowers Table
CREATE TABLE borrowers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('Quartermaster', 'Patrol Leader', 'Scout Leader')),
    phone VARCHAR(20) NOT NULL
);

-- Gear Loan Requests Table
CREATE TABLE loan_records (
    id SERIAL PRIMARY KEY,
    borrower_id INT REFERENCES borrowers(id) ON DELETE CASCADE,
    quartermaster_id INT REFERENCES borrowers(id) ON DELETE SET NULL, -- Approver
    purpose VARCHAR(100) NOT NULL, -- e.g., District Campout
    loan_date DATE NOT NULL,
    expected_return_date DATE NOT NULL,
    actual_return_date DATE,
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Active', 'Returned', 'Overdue', 'Rejected'))
);

-- Loaned Items (Junction Table for Multi-Item Checkout)
CREATE TABLE loan_items (
    loan_id INT REFERENCES loan_records(id) ON DELETE CASCADE,
    item_id INT REFERENCES inventory_items(id) ON DELETE CASCADE,
    condition_out VARCHAR(20) NOT NULL,
    condition_in VARCHAR(20),
    PRIMARY KEY (loan_id, item_id)
);

-- Maintenance / Damage Reports
CREATE TABLE maintenance_logs (
    id SERIAL PRIMARY KEY,
    item_id INT REFERENCES inventory_items(id) ON DELETE CASCADE,
    reported_by INT REFERENCES borrowers(id) ON DELETE SET NULL,
    issue_description TEXT NOT NULL,
    repair_cost DECIMAL(8, 2) DEFAULT 0.00,
    resolved BOOLEAN DEFAULT FALSE,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. API Endpoint Mapping

| Method | Endpoint | Description | Request Payload / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/inventory` | Add new gear entry to inventory | `{ item_code, name, category_id, condition, storage_location }` |
| `GET` | `/api/inventory` | Search & filter gear status | `?category=Tents&status=Available` |
| `POST` | `/api/loans` | Submit a gear loan request | `{ borrower_id, purpose, loan_date, return_date, item_ids }` |
| `PATCH` | `/api/loans/{id}/approve` | Approve gear checkout (QM) | `{ quartermaster_id }` |
| `PATCH` | `/api/loans/{id}/return` | Process gear return & inspect condition | `{ returned_items: [{ item_id, condition_in }] }` |
| `POST` | `/api/maintenance` | Log a damaged/repair item report | `{ item_id, issue_description }` |
| `DELETE` | `/api/inventory/{id}` | Retire lost or unrepairable item | Header: `Authorization: Bearer <QM_JWT>` |

---

## 5. CRUD Functionality Breakdown

* **Create**:
  * Quartermasters register new gear items with unique codes and categories.
  * Patrol Leaders submit multi-item loan requests for upcoming campouts.
  * Log maintenance issues and damage reports.
* **Read**:
  * Filter active stock levels by category, condition, and availability.
  * View active loan logs and overdue items.
* **Update**:
  * Quartermasters process returns, marking items back to `Available` or updating condition to `Needs Repair`.
  * Extend loan return dates for multi-week projects.
* **Delete**:
  * Retire lost or beyond-repair equipment from active inventory.
  * Cancel unapproved loan requests.