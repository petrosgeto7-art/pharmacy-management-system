import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/layout/ProtectedRoute';
import Login from './pages/auth/Login';
import Dashboard from './pages/dashboard/Dashboard';
import POS from './pages/sales/POS';
import { 
  LayoutDashboard, ShoppingCart, Package, Users, 
  Truck, Activity, FileText, Settings, LogOut, Pill
} from 'lucide-react';

const SidebarItem = ({ to, icon: Icon, label }: { to: string, icon: any, label: string }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link 
      to={to} 
      className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
        isActive 
          ? 'bg-primary text-primary-foreground shadow-md' 
          : 'text-muted-foreground hover:bg-muted hover:text-foreground'
      }`}
    >
      <Icon size={20} className={isActive ? 'opacity-100' : 'opacity-70'} />
      <span className="font-medium">{label}</span>
    </Link>
  );
};

const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout } = useAuth();
  
  return (
    <div className="flex h-screen overflow-hidden bg-zinc-50 dark:bg-zinc-950 text-foreground">
      {/* Sidebar */}
      <aside className="w-72 border-r bg-card flex flex-col shadow-sm z-10">
        <div className="p-6 flex items-center gap-3">
          <div className="h-10 w-10 bg-primary/10 text-primary flex items-center justify-center rounded-xl">
            <Pill size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">CarePlus</h1>
            <p className="text-xs text-muted-foreground font-medium">Pharmacy System</p>
          </div>
        </div>
        
        <nav className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-1.5">
          <SidebarItem to="/" icon={LayoutDashboard} label="Dashboard" />
          <SidebarItem to="/pos" icon={ShoppingCart} label="Point of Sale" />
          <div className="my-2 border-t"></div>
          <p className="px-4 text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-2 mt-2">Inventory</p>
          <SidebarItem to="/medicines" icon={Package} label="Medicines" />
          <SidebarItem to="/suppliers" icon={Truck} label="Suppliers & Purchases" />
          
          <div className="my-2 border-t"></div>
          <p className="px-4 text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-2 mt-2">Management</p>
          <SidebarItem to="/customers" icon={Users} label="Customers" />
          <SidebarItem to="/prescriptions" icon={Activity} label="Prescriptions" />
          <SidebarItem to="/reports" icon={FileText} label="Reports" />
          
          {user?.is_admin && (
            <>
              <div className="my-2 border-t"></div>
              <SidebarItem to="/settings" icon={Settings} label="Settings" />
            </>
          )}
        </nav>
        
        <div className="p-4 border-t bg-muted/30">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-10 w-10 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold">
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.first_name} {user?.last_name}</p>
              <p className="text-xs text-muted-foreground truncate">{user?.role}</p>
            </div>
          </div>
          <button 
            onClick={logout}
            className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-md border bg-background hover:bg-muted text-sm font-medium transition-colors text-destructive"
          >
            <LogOut size={16} />
            Sign Out
          </button>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="h-full p-8 max-w-[1600px] mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            
            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<MainLayout><Dashboard /></MainLayout>} />
              <Route path="/pos" element={<MainLayout><POS /></MainLayout>} />
              
              {/* Placeholders for other routes */}
              <Route path="/medicines" element={<MainLayout><div>Medicines Module - Coming Soon</div></MainLayout>} />
              <Route path="/suppliers" element={<MainLayout><div>Suppliers Module - Coming Soon</div></MainLayout>} />
              <Route path="/customers" element={<MainLayout><div>Customers Module - Coming Soon</div></MainLayout>} />
              <Route path="/prescriptions" element={<MainLayout><div>Prescriptions Module - Coming Soon</div></MainLayout>} />
              <Route path="/reports" element={<MainLayout><div>Reports Module - Coming Soon</div></MainLayout>} />
              <Route path="/settings" element={<MainLayout><div>Settings Module - Coming Soon</div></MainLayout>} />
              
              {/* Fallback route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
