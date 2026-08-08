import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '@/api/client';
import { API_URLS } from '@/api/urls';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  LineChart, Line
} from 'recharts';
import { 
  Package, DollarSign, Users, AlertTriangle, Activity,
  TrendingUp, TrendingDown, Clock, ShoppingCart
} from 'lucide-react';

export default function Dashboard() {
  const { data: summary, isLoading, error } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: async () => {
      const response = await api.get(API_URLS.DASHBOARD_SUMMARY);
      return response.data;
    }
  });

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return <div className="text-destructive p-4 border rounded-md">Error loading dashboard data.</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight text-foreground">Dashboard</h2>
        <p className="text-muted-foreground">Welcome to CarePlus Pharmacy management system.</p>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Revenue */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 flex flex-col">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="tracking-tight text-sm font-medium">Today's Revenue</h3>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="text-2xl font-bold">${summary.today_revenue.toFixed(2)}</div>
          <p className="text-xs text-muted-foreground mt-1 text-green-600 flex items-center">
            <TrendingUp className="h-3 w-3 mr-1" /> Gross sales
          </p>
        </div>

        {/* Profit */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 flex flex-col">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="tracking-tight text-sm font-medium">Today's Profit</h3>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="text-2xl font-bold">${summary.today_profit.toFixed(2)}</div>
          <p className="text-xs text-muted-foreground mt-1">Est. gross profit</p>
        </div>

        {/* Inventory Value */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 flex flex-col">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="tracking-tight text-sm font-medium">Inventory Value</h3>
            <Package className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="text-2xl font-bold">${summary.inventory_value.toFixed(2)}</div>
          <p className="text-xs text-muted-foreground mt-1">{summary.medicines_count} medicines in stock</p>
        </div>

        {/* Customers */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 flex flex-col">
          <div className="flex flex-row items-center justify-between pb-2">
            <h3 className="tracking-tight text-sm font-medium">Total Customers</h3>
            <Users className="h-4 w-4 text-muted-foreground" />
          </div>
          <div className="text-2xl font-bold">{summary.customers_count}</div>
          <p className="text-xs text-muted-foreground mt-1">Registered patients</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        {/* Main Chart */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm col-span-4 p-6">
          <div className="flex flex-col space-y-1.5 mb-4">
            <h3 className="font-semibold leading-none tracking-tight">Sales Overview</h3>
            <p className="text-sm text-muted-foreground">Last 7 days revenue</p>
          </div>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={summary.sales_chart}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
                <XAxis dataKey="date" axisLine={false} tickLine={false} tickMargin={10} fontSize={12} />
                <YAxis axisLine={false} tickLine={false} tickMargin={10} fontSize={12} tickFormatter={(value) => `$${value}`} />
                <RechartsTooltip cursor={{fill: 'var(--accent)'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
                <Bar dataKey="total" fill="var(--primary)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alerts & Notifications Panel */}
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm col-span-3 p-6 flex flex-col">
          <div className="flex flex-col space-y-1.5 mb-4">
            <h3 className="font-semibold leading-none tracking-tight">Action Items</h3>
            <p className="text-sm text-muted-foreground">Requires your attention</p>
          </div>
          
          <div className="flex-1 space-y-4 overflow-y-auto pr-2">
            {summary.expiring_medicines_count > 0 && (
              <div className="flex items-start space-x-4 border border-orange-200 bg-orange-50 dark:bg-orange-950/20 dark:border-orange-900/50 p-3 rounded-lg">
                <AlertTriangle className="text-orange-500 mt-0.5 h-5 w-5" />
                <div className="flex-1">
                  <h4 className="text-sm font-semibold text-orange-800 dark:text-orange-400">Expiring Stock</h4>
                  <p className="text-xs text-orange-700 dark:text-orange-300 mt-1">{summary.expiring_medicines_count} batches are expiring within 30 days.</p>
                </div>
              </div>
            )}
            
            {summary.expired_medicines_count > 0 && (
              <div className="flex items-start space-x-4 border border-destructive/30 bg-destructive/10 p-3 rounded-lg">
                <AlertTriangle className="text-destructive mt-0.5 h-5 w-5" />
                <div className="flex-1">
                  <h4 className="text-sm font-semibold text-destructive">Expired Stock</h4>
                  <p className="text-xs text-destructive/80 mt-1">{summary.expired_medicines_count} batches have expired and must be disposed.</p>
                </div>
              </div>
            )}

            {summary.pending_prescriptions > 0 && (
              <div className="flex items-start space-x-4 border bg-card p-3 rounded-lg">
                <Clock className="text-blue-500 mt-0.5 h-5 w-5" />
                <div className="flex-1">
                  <h4 className="text-sm font-semibold">Pending Prescriptions</h4>
                  <p className="text-xs text-muted-foreground mt-1">{summary.pending_prescriptions} prescriptions waiting to be dispensed.</p>
                </div>
              </div>
            )}
            
            {summary.expiring_medicines_count === 0 && summary.expired_medicines_count === 0 && summary.pending_prescriptions === 0 && (
              <div className="flex flex-col items-center justify-center h-40 text-center">
                <div className="h-12 w-12 rounded-full bg-green-100 dark:bg-green-900/20 flex items-center justify-center mb-3">
                  <svg className="h-6 w-6 text-green-600 dark:text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h4 className="text-sm font-medium">All caught up!</h4>
                <p className="text-xs text-muted-foreground mt-1">No pending action items right now.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
