# Project Plan: KemPengakap

## 1. Overview & Real-World Problem
District and state-level scout gatherings (*Perkhemahan Berek*, *Jambori*) in Malaysia involve managing hundreds of participants, contingent registrations, campsite allocations, and activity rotations. Currently, camp organizers rely on fragmented Google Sheets, paper sign-in sheets, and WhatsApp groups. This results in registration bottlenecks, lost emergency contact information, dynamic schedule updates failing to reach contingents, and delayed check-ins.

**KemPengakap** is a full-stack event and operations management platform designed for scout campouts, jamborees, and district training camps.

---

## 2. Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js (TypeScript), Tailwind CSS | Contingent dashboard, QR code check-in scanner UI, duty rosters |
| **Backend** | Python (FastAPI / Django REST Framework) | Dynamic capacity management, real-time schedule tracking, auth |
| **Database** | PostgreSQL | Relational storage for events, contingents, participants, and sub-camps |
| **Auth** | JWT with Multi-Tier Roles | Event Organizers, Contingent Leaders (*Pemimpin*), and Scouts |

---

## 3. Database Schema

```sql
-- Camps / Events Table
CREATE TABLE camp_events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    max_capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sub-Camps Table
CREATE TABLE sub_camps (
    id SERIAL PRIMARY KEY,
    camp_id INT REFERENCES camp_events(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL, -- e.g., Sub-Camp Temenggong
    capacity INT NOT NULL
);

-- Contingents Table (Groups from schools/districts)
CREATE TABLE contingents (
    id SERIAL PRIMARY KEY,
    camp_id INT REFERENCES camp_events(id) ON DELETE CASCADE,
    troop_name VARCHAR(100) NOT NULL,
    leader_name VARCHAR(100) NOT NULL,
    leader_phone VARCHAR(20) NOT NULL,
    sub_camp_id INT REFERENCES sub_camps(id) ON DELETE SET NULL,
    payment_status VARCHAR(20) DEFAULT 'Pending' CHECK (payment_status IN ('Pending', 'Paid', 'Partial'))
);

-- Camp Participants Table
CREATE TABLE camp_participants (
    id SERIAL PRIMARY KEY,
    contingent_id INT REFERENCES contingents(id) ON DELETE CASCADE,
    full_name VARCHAR(100) NOT NULL,
    ic_number VARCHAR(15) NOT NULL,
    category VARCHAR(20) CHECK (category IN ('Scout', 'Leader', 'Quartermaster', 'Staff')),
    dietary_restriction VARCHAR(50) DEFAULT 'None',
    emergency_contact VARCHAR(20) NOT NULL,
    checked_in BOOLEAN DEFAULT FALSE,
    checked_in_at TIMESTAMP
);

-- Activity Rotations
CREATE TABLE camp_activities (
    id SERIAL PRIMARY KEY,
    camp_id INT REFERENCES camp_events(id) ON DELETE CASCADE,
    activity_name VARCHAR(100) NOT NULL, -- e.g., Night Trekking, Pioneering
    max_slots INT NOT NULL,
    scheduled_time TIMESTAMP NOT NULL
);

-- Participant Duty Roster
CREATE TABLE duty_rosters (
    id SERIAL PRIMARY KEY,
    camp_id INT REFERENCES camp_events(id) ON DELETE CASCADE,
    contingent_id INT REFERENCES contingents(id) ON DELETE CASCADE,
    duty_type VARCHAR(50) NOT NULL, -- e.g., Sentri (Night Watch), Kitchen Duty
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);
```

---

## 4. API Endpoint Mapping

| Method | Endpoint | Description | Request Payload / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/camps` | Create a new campout event | `{ title, location, start_date, end_date, capacity }` |
| `GET` | `/api/camps` | List all upcoming and ongoing campouts | `?status=upcoming` |
| `POST` | `/api/contingents` | Register a troop contingent for a camp | `{ camp_id, troop_name, leader_name, leader_phone }` |
| `POST` | `/api/participants` | Add scout participant details | `{ contingent_id, full_name, ic_number, category, emergency_contact }` |
| `PATCH` | `/api/participants/{id}/checkin` | Record participant check-in on-site | `{ checked_in: true }` |
| `GET` | `/api/camps/{id}/roster` | Fetch active duty and activity roster | `{ camp_id }` |
| `PATCH` | `/api/contingents/{id}` | Update contingent sub-camp assignment or payment | `{ sub_camp_id, payment_status }` |
| `DELETE` | `/api/contingents/{id}` | Withdraw contingent from campout | Header: `Authorization: Bearer <LeaderJWT>` |

---

## 5. CRUD Functionality Breakdown

* **Create**:
  * Event organizers create camp events, define sub-camps, and add activity slots.
  * Troop leaders register contingent groups and upload member details.
  * Organizers construct sentry and kitchen duty rosters.
* **Read**:
  * Troop leaders view schedules, sub-camp locations, and participant check-in statuses.
  * Organizers view real-time camp check-in counters and dietary breakdown charts.
* **Update**:
  * Gate staff update participant check-in status using QR scans upon arrival.
  * Organizers reassign contingents to different sub-camps or update payment details.
* **Delete**:
  * Cancel activity sessions due to inclement weather.
  * Remove withdrawn participants or contingents.