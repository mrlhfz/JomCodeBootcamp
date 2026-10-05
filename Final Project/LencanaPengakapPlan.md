# Project Plan: LencanaPengakap

## 1. Overview & Real-World Problem
The Malaysian Scouting movement (*Persekutuan Pengakap Malaysia - PPM*) relies heavily on physical logbooks (*Buku Log*) and paper testing sheets to record badge progress across scout categories (*Kanak-Kanak*, *Muda*, *Remaja*, *Kelana*). Paper records are often damaged or lost during outdoor campouts. Furthermore, verifying requirement completions during candidate review for top awards such as **Anugerah Pengakap Raja** (King's Scout Award) creates a massive administrative burden for district examiners (*Pemeriksa Daerah*).

**LencanaPengakap** is a digital progress book and badge verification platform connecting Scouts, Scout Leaders (*Pemimpin*), and District Examiners.

---

## 2. Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js (TypeScript), Tailwind CSS | Interactive badge progress tree, media proof submission UI |
| **Backend** | Python (FastAPI / Django REST Framework) | Verification approval workflows, PDF report generation |
| **Database** | PostgreSQL | Relational tracking for troops, badge frameworks, and approvals |
| **Auth** | JWT with Multi-Tier Roles | Scout, Scout Leader, and District Examiner access permissions |

---

## 3. Database Schema

```sql
-- Troops Table
CREATE TABLE troops (
    id SERIAL PRIMARY KEY,
    troop_number VARCHAR(20) NOT NULL,
    school_or_area VARCHAR(100) NOT NULL,
    district VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL
);

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('Scout', 'Leader', 'Examiner', 'Admin')),
    troop_id INT REFERENCES troops(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Badges Master Table
CREATE TABLE badges (
    id SERIAL PRIMARY KEY,
    badge_name VARCHAR(100) NOT NULL,
    category VARCHAR(30) CHECK (category IN ('Kanak-Kanak', 'Muda', 'Remaja', 'Kelana', 'Raja')),
    description TEXT
);

-- Badge Tasks / Requirements
CREATE TABLE badge_tasks (
    id SERIAL PRIMARY KEY,
    badge_id INT REFERENCES badges(id) ON DELETE CASCADE,
    task_number INT NOT NULL,
    description TEXT NOT NULL
);

-- Task Submissions & Sign-Offs
CREATE TABLE task_submissions (
    id SERIAL PRIMARY KEY,
    scout_id INT REFERENCES users(id) ON DELETE CASCADE,
    task_id INT REFERENCES badge_tasks(id) ON DELETE CASCADE,
    evidence_url TEXT, -- Link to photo/video proof
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
    verified_by INT REFERENCES users(id) ON DELETE SET NULL, -- Leader or Examiner ID
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP
);
```

---

## 4. API Endpoint Mapping

| Method | Endpoint | Description | Request Payload / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register user account with role | `{ full_name, email, password, role, troop_id }` |
| `GET` | `/api/badges` | Fetch badge requirements list | `?category=Remaja` |
| `POST` | `/api/submissions` | Scout submits task proof | `{ task_id, evidence_url }` |
| `GET` | `/api/submissions/troop` | Leader views pending troop submissions | Header: `Authorization: Bearer <LeaderJWT>` |
| `PATCH` | `/api/submissions/{id}/verify` | Leader/Examiner signs off on task | `{ status: "Approved" | "Rejected" }` |
| `GET` | `/api/scouts/{id}/progress` | View complete badge tree & status | `{ scout_id }` |
| `DELETE` | `/api/submissions/{id}` | Delete invalid draft submission | Header: `Authorization: Bearer <ScoutJWT>` |

---

## 5. CRUD Functionality Breakdown

* **Create**:
  * Scouts upload badge task submission entries with media evidence links.
  * Leaders create digital badge testing sessions and troop entries.
* **Read**:
  * Scouts view their interactive badge progress dashboard.
  * Scout Leaders view pending submission queues for their troop.
  * District Examiners view King's Scout candidate digital portfolio records.
* **Update**:
  * Leaders sign off on task submissions (updates status from `Pending` to `Approved`).
  * Scouts update draft or rejected submissions with revised proof.
* **Delete**:
  * Scouts withdraw pending or draft submissions.
  * Admins archive records of scouts who have aged out.