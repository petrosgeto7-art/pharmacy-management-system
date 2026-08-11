# 💊 CarePlus Pharmacy Management System

A comprehensive, production-quality Pharmacy Management System built with **Django REST Framework** (Backend) and **React + TypeScript** (Frontend).

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

- **Role-Based Access Control (RBAC)** — Super Admin, Manager, Pharmacist, Cashier, Inventory Manager
- **Point of Sale (POS)** — Real-time checkout with barcode scanning support
- **Inventory Management** — FEFO (First Expire, First Out) batch tracking
- **Prescription Management** — Doctor prescription tracking and dispensing workflow
- **Purchase Orders** — Supplier management with automated stock replenishment
- **Financial Reports** — Revenue, profit, and expense tracking with chart visualizations
- **Audit Logging** — Complete trail of all system actions
- **JWT Authentication** — Secure token-based auth with automatic refresh
- **Dashboard** — Real-time KPIs, expiring stock alerts, and sales charts

## 📁 Project Structure

```
├── backend/                 # Django REST Framework API
│   ├── accounts/            # User & Role management
│   ├── medicines/           # Medicine catalog
│   ├── inventory/           # Batch & stock tracking
│   ├── sales/               # POS & sale transactions
│   ├── purchases/           # Purchase orders
│   ├── prescriptions/       # Prescription management
│   ├── customers/           # Customer records
│   ├── suppliers/           # Supplier records
│   ├── returns/             # Return processing
│   ├── expenses/            # Expense tracking
│   ├── reports/             # Financial reports
│   ├── dashboard/           # Dashboard aggregation
│   ├── notifications/       # System notifications
│   ├── audit/               # Audit trail
│   └── pharmacy/            # Pharmacy settings
├── frontend/                # React + TypeScript + Vite
│   ├── src/
│   │   ├── api/             # Axios client & URL constants
│   │   ├── contexts/        # Auth context provider
│   │   ├── components/      # Reusable UI components
│   │   └── pages/           # Page components
│   └── ...
└── README.md
```

## 🛠️ Quick Start

### Backend
```bash
cd backend
python -m venv ../venv
../venv/Scripts/activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Default Login
| Username | Password     | Role         |
|----------|-------------|--------------|
| admin    | password123 | Super Admin  |
| manager  | password123 | Manager      |
| pharmacist | password123 | Pharmacist |
| cashier  | password123 | Cashier      |

## 📝 License

This project is licensed under the MIT License.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
