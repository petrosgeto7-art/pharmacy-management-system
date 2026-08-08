# API Documentation

The backend exposes a RESTful API using Django REST Framework. Authentication is handled via JWT.

## Base URL
`/api/`

## Authentication (`/api/auth/`)
- `POST /login/` - Obtain JWT tokens (access, refresh)
- `POST /refresh/` - Refresh access token

## Users & Roles (`/api/users/`, `/api/roles/`)
- `GET /users/me/` - Get current user profile
- `POST /users/change_password/` - Update password
- Standard CRUD for Users and Roles (Requires Admin)

## Pharmacy & Settings (`/api/pharmacy/`)
- `GET /` - Retrieve pharmacy details (Name, contact, license)
- `PUT /` - Update pharmacy details

## Medicines Catalog (`/api/medicines/`, `/api/categories/`, `/api/manufacturers/`)
- `GET /` - List with filtering (by category, manufacturer, status)
- `POST /` - Add a new medicine
- `GET /:id/` - Get detailed medicine info including stock status

## Inventory (`/api/batches/`, `/api/inventory/`)
- `GET /batches/expiring_soon/` - List batches expiring in 30 days
- `GET /batches/expired/` - List expired batches
- `GET /inventory/movements/` - Audit log of stock ins/outs

## Point of Sale (`/api/sales/`)
- `POST /` - Process a new sale (Automatically performs FEFO batch deduction and generates stock movements)

## Supply Chain (`/api/purchases/`, `/api/suppliers/`)
- `POST /purchases/:id/complete/` - Mark a purchase order as received, automatically updates inventory and supplier balances.

## Prescriptions (`/api/prescriptions/`)
- `POST /:id/dispense/` - Mark prescription as dispensed.

## Reports (`/api/dashboard/`, `/api/reports/`)
- `GET /dashboard/summary/` - Aggregated stats for the frontend dashboard
- `GET /reports/sales/` - Sales breakdown
- `GET /reports/financial/` - Profit margins and expense tracking
