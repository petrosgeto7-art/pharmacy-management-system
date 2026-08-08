export const API_URLS = {
  // Auth
  LOGIN: '/auth/login/',
  REFRESH: '/auth/refresh/',
  ME: '/users/me/',
  
  // Dashboard
  DASHBOARD_SUMMARY: '/dashboard/summary/',
  
  // Entities
  MEDICINES: '/medicines/',
  CATEGORIES: '/categories/',
  MANUFACTURERS: '/manufacturers/',
  SUPPLIERS: '/suppliers/',
  CUSTOMERS: '/customers/',
  
  // Inventory
  BATCHES: '/batches/',
  EXPIRING_BATCHES: '/batches/expiring_soon/',
  EXPIRED_BATCHES: '/batches/expired/',
  STOCK_MOVEMENTS: '/inventory/movements/',
  
  // Transactions
  PURCHASES: '/purchases/',
  SALES: '/sales/',
  PRESCRIPTIONS: '/prescriptions/',
  RETURNS: '/returns/',
  EXPENSES: '/expenses/',
  
  // Users & Admin
  USERS: '/users/',
  ROLES: '/roles/',
  AUDIT_LOGS: '/audit-logs/',
  PHARMACY_SETTINGS: '/pharmacy/',
  
  // Reports
  REPORT_SALES: '/reports/sales/',
  REPORT_FINANCIAL: '/reports/financial/',
};
