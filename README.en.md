# PetVida — Veterinary Hospital

Management system in Python + PostgreSQL.

**English** · [Português](README.md)

---

## Authors
Eduardo Souza de Barros  
Gabriel Stoffel Cirilo

---


## Overview

PetVida is a veterinary management system developed in Python integrated with a PostgreSQL database.  
It manages pet owners, animals, consultations, surgeries and users, with role-based access control (Administrator, Owner and Veterinarian).

The system was designed for academic purposes, following good practices of database modeling, referential integrity and modular code structure.

---

## System architecture

The system is split into modules to make it easier to maintain, read and organize:

```
petvida/
│  config.py        → PostgreSQL configuration and connection
│  main.py          → Entry point and application flow
│  menus.py         → All menus and navigation
│  services.py      → Business rules and SQL operations
│  utils.py         → Validation functions and utilities
```

---

## Technologies used

### Backend
- Python 3  
- psycopg2 (PostgreSQL integration)  
- bcrypt (secure password hashing)

### Database
- PostgreSQL  
- Schema used: `petvida`

### Additional tools
- pgAdmin  
- Git / GitHub  

---

## Installation

Install the project dependencies:

```bash
pip install psycopg2 bcrypt
```

Make sure PostgreSQL is installed and running.

---

## Configuration

Set the PostgreSQL password in the `PETVIDA_DB_PASSWORD` environment variable:

```bash
export PETVIDA_DB_PASSWORD="your_password"  # Linux / macOS
set PETVIDA_DB_PASSWORD=your_password       # Windows (cmd)
```

The other connection settings are in `config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": os.environ.get("PETVIDA_DB_PASSWORD", ""),
    "options": "-c search_path=petvida"
}
```

Then run the SQL script `dbcode.txt` (at the repository root) in PostgreSQL, for example through pgAdmin or with:

```bash
psql -U postgres -f dbcode.txt
```

This script creates:

- The `petvida` schema
- All system tables
- Constraints
- Indexes
- Final adjustments with ALTER TABLE

---

## Execution

To start the system:

```bash
cd petvida
python main.py
```

On the first run:

- The schema is created (if it doesn't exist)
- The tables are created automatically
- A default administrator is generated
- The main menu is displayed

After logging in, each user sees the menu for their role.

---

## Database modeling

Based on the mini-world description, the ER model and the ER diagram developed for the academic project.

### Main entities
- Owner (`dono`)
- Animal
- Consultation (`consulta`)
- Surgery (`cirurgia`)
- User (Administrator, Owner and Veterinarian)

### Key relationships
- Owner → Animal  
- Animal → Consultation  
- Animal → Surgery  
- User (Owner) → Owner  

All integrity is enforced with foreign keys and ON DELETE CASCADE policies.

---

## Features

### Administrator
- Create, edit and delete users  
- Manage owners  
- Manage animals  
- Register consultations  
- Register surgeries  
- Reports:
  - Animals per owner  
  - Consultations by period  
  - Search by CPF (Brazilian individual taxpayer ID)  
- Full table cleanup for maintenance  

---

### Owner (Client)
- View personal data  
- Update information  
- Register animals  
- View registered animals  
- Check consultations  
- Cancel consultations  

---

### Veterinarian
- View registered animals  
- Register consultations  
- Register surgeries  
- View their own appointments  
- Filter consultations by period  

---

## Security

The system implements:

- Secure password hashing with `bcrypt`  
- Login blocking after multiple failed attempts  
- Input validation in every menu  
- Strict permission control by user type  
- Integrity enforced by PostgreSQL constraints  

---

## Directory structure
```
petvida/
├── petvida/                # Main application source folder
│   ├── config.py           # Database settings
│   ├── main.py             # Entry point that starts the system
│   ├── menus.py            # Menus and per-role navigation
│   ├── services.py         # Business rules and SQL operations
│   ├── utils.py            # Helper functions (validation, input, etc.)
│
├── docs/                   # Project documentation (ER model, ER diagram, mini-world, report, etc.)
│   └── *.docx files*
│
├── dbcode.txt              # SQL script that creates the schema, tables and constraints
│
├── README.md               # Main repository documentation
│
```

The code, the database names and the documentation in `docs/` are in Portuguese.

---

## License

Academic project developed for the Database Project course at CESMAC.  
Use for study purposes is permitted, provided the authors are credited:  
Eduardo Souza de Barros  
Gabriel Stoffel Cirilo
