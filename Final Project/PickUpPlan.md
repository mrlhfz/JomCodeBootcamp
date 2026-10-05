# Project Plan: PickUp MY

## 1. Overview & Real-World Problem
In Malaysia, finding available outdoor and indoor basketball courts (e.g., Dewan Komuniti Batu Muda, Kompleks 3K MBSJ) and organizing 3x3 or 5v5 games is highly fragmented. Casual players rely on disjointed WhatsApp groups, while municipal courts lack live availability status. Courts are often either overcrowded or occupied by private coaching classes without prior notice.

**PickUp MY** solves this by offering a real-time pick-up court aggregator and game matchmaking platform tailored to local streetball communities.

---

## 2. Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React / Next.js (TypeScript), Tailwind CSS, React-Leaflet | Dynamic UI, map view for nearby courts, modal forms |
| **Backend** | Python (FastAPI / Django REST Framework) | Async endpoints, geo-distance calculations, JWT authentication |
| **Database** | PostgreSQL (with PostGIS extensions) | Relational database to store users, courts, games, and check-ins |
| **Auth** | JWT (JSON Web Tokens) | Secure user authentication and role management |

---

## 3. Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    skill_level VARCHAR(20) CHECK (skill_level IN ('Beginner', 'Intermediate', 'Advanced', 'Open')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courts Table
CREATE TABLE courts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    court_type VARCHAR(20) CHECK (court_type IN ('Indoor', 'Outdoor', 'Covered')),
    has_lighting BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Game Sessions Table
CREATE TABLE game_sessions (
    id SERIAL PRIMARY KEY,
    host_id INT REFERENCES users(id) ON DELETE CASCADE,
    court_id INT REFERENCES courts(id) ON DELETE CASCADE,
    game_type VARCHAR(10) CHECK (game_type IN ('3x3', '5v5', 'Half-Court')),
    target_players INT DEFAULT 6,
    scheduled_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'Upcoming' CHECK (status IN ('Upcoming', 'In Progress', 'Completed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session Players (Junction Table)
CREATE TABLE session_players (
    session_id INT REFERENCES game_sessions(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (session_id, user_id)
);

-- Court Check-Ins (Live Status)
CREATE TABLE court_checkins (
    id SERIAL PRIMARY KEY,
    court_id INT REFERENCES courts(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    crowd_level VARCHAR(20) CHECK (crowd_level IN ('Empty', 'Moderate', 'Full', 'Under Maintenance')),
    checked_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. API Endpoint Mapping

| Method | Endpoint | Description | Request Payload / Params |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register a new user profile | `{ username, email, password, skill_level }` |
| `POST` | `/api/auth/login` | Authenticate user & return JWT token | `{ email, password }` |
| `GET` | `/api/courts` | Search nearby courts | `?lat=3.139&lng=101.686&radius=10` |
| `POST` | `/api/courts` | Add a new community court | `{ name, address, latitude, longitude, court_type }` |
| `GET` | `/api/sessions` | List open pickup games | `?court_id=1&status=Upcoming` |
| `POST` | `/api/sessions` | Host a new pickup game | `{ court_id, game_type, target_players, scheduled_time }` |
| `PUT` | `/api/sessions/{id}/join` | Reserve a slot in a game | Header: `Authorization: Bearer <JWT>` |
| `PATCH` | `/api/sessions/{id}` | Update session parameters | `{ scheduled_time, target_players }` |
| `DELETE` | `/api/sessions/{id}` | Cancel hosted session | Header: `Authorization: Bearer <JWT>` |
| `POST` | `/api/checkins` | Post a live court crowd check-in | `{ court_id, crowd_level }` |

---

## 5. CRUD Functionality Breakdown

* **Create**:
  * Users host games specifying court location, format, required player count, and time slot.
  * Register unlisted community courts with geo-coordinates.
  * Submit live crowd check-ins.
* **Read**:
  * Query nearby courts on an interactive Leaflet map.
  * Filter active game listings by skill level, proximity, and time slot.
  * View court detail pages with crowd updates from the past 2 hours.
* **Update**:
  * Join or leave active game sessions (modifies player count).
  * Hosts can edit game details (e.g., change start time due to rain).
* **Delete**:
  * Cancel hosted game sessions.
  * Remove individual player reservations.