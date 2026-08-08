import { useState, useMemo } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import api from '@/api/client';
import { API_URLS } from '@/api/urls';
import { 
  Search, Plus, Minus, Trash2, ShoppingCart, 
  CreditCard, Banknote, FileText
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const saleItemSchema = z.object({
  medicine: z.number(),
  medicine_name: z.string(),
  quantity: z.number().min(1),
  unit_price: z.number().min(0),
  max_quantity: z.number(),
});

const saleSchema = z.object({
  customer: z.number().nullable().optional(),
  prescription: z.number().nullable().optional(),
  payment_method: z.enum(['cash', 'card', 'insurance', 'mobile']),
  amount_paid: z.number().min(0),
  notes: z.string().optional(),
  items: z.array(saleItemSchema).min(1, "Add at least one item to the cart"),
});

type SaleForm = z.infer<typeof saleSchema>;

export default function POS() {
  const { user } = useAuth();
  const [searchTerm, setSearchTerm] = useState('');
  
  const { data: medicines } = useQuery({
    queryKey: ['medicines-pos'],
    queryFn: async () => {
      const response = await api.get(API_URLS.MEDICINES);
      return response.data;
    }
  });

  const { register, control, handleSubmit, watch, setValue, formState: { errors } } = useForm<SaleForm>({
    resolver: zodResolver(saleSchema),
    defaultValues: {
      customer: null,
      payment_method: 'cash',
      amount_paid: 0,
      items: [],
    }
  });

  const { fields, append, remove, update } = useFieldArray({
    control,
    name: "items"
  });

  const items = watch('items');
  const amountPaid = watch('amount_paid');

  const subtotal = useMemo(() => {
    return items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0);
  }, [items]);

  const tax = subtotal * 0.05; // Example 5% tax
  const total = subtotal + tax;
  const change = Math.max(0, amountPaid - total);

  // Filter medicines for search
  const filteredMedicines = useMemo(() => {
    if (!medicines) return [];
    if (!searchTerm) return medicines.slice(0, 10); // Show top 10 by default
    return medicines.filter((m: any) => 
      m.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
      (m.barcode && m.barcode.includes(searchTerm))
    ).slice(0, 10);
  }, [medicines, searchTerm]);

  const addToCart = (medicine: any) => {
    if (medicine.total_stock <= 0) {
      alert("Out of stock!");
      return;
    }
    
    const existingIndex = items.findIndex(item => item.medicine === medicine.id);
    if (existingIndex >= 0) {
      if (items[existingIndex].quantity < medicine.total_stock) {
        const newItem = { ...items[existingIndex], quantity: items[existingIndex].quantity + 1 };
        update(existingIndex, newItem);
      } else {
        alert("Cannot exceed available stock.");
      }
    } else {
      append({
        medicine: medicine.id,
        medicine_name: medicine.name,
        quantity: 1,
        unit_price: Number(medicine.selling_price),
        max_quantity: medicine.total_stock
      });
    }
  };

  const processSale = useMutation({
    mutationFn: async (data: SaleForm) => {
      const payload = {
        ...data,
        subtotal,
        tax,
        discount: 0,
        total,
        payment_status: data.amount_paid >= total ? 'paid' : 'partial',
        change_due: change
      };
      const response = await api.post(API_URLS.SALES, payload);
      return response.data;
    },
    onSuccess: () => {
      alert("Sale processed successfully!");
      setValue('items', []);
      setValue('amount_paid', 0);
    },
    onError: (error: any) => {
      alert("Error processing sale: " + (error.response?.data?.error || "Unknown error"));
    }
  });

  const onSubmit = (data: SaleForm) => {
    processSale.mutate(data);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-3xl font-bold tracking-tight">Point of Sale</h2>
        <div className="text-sm text-muted-foreground flex items-center">
          <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
          Terminal Active - Cashier: {user?.first_name}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 flex-1 min-h-0">
        
        {/* Left Side: Product Search & Grid */}
        <div className="md:col-span-7 lg:col-span-8 flex flex-col min-h-0 border rounded-xl bg-card overflow-hidden">
          <div className="p-4 border-b bg-muted/30">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search medicines by name, SKU, or scan barcode..."
                className="w-full pl-10 pr-4 py-3 rounded-lg border bg-background focus:outline-none focus:ring-2 focus:ring-primary shadow-sm text-lg"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                autoFocus
              />
            </div>
          </div>
          
          <div className="flex-1 overflow-auto p-4 bg-zinc-50 dark:bg-zinc-950">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {filteredMedicines.map((med: any) => (
                <div 
                  key={med.id} 
                  onClick={() => addToCart(med)}
                  className={`relative p-4 rounded-xl border bg-card shadow-sm cursor-pointer transition-all hover:shadow-md hover:border-primary ${med.total_stock <= 0 ? 'opacity-50 grayscale' : ''}`}
                >
                  <div className="font-semibold text-sm line-clamp-2 min-h-[2.5rem]">{med.name}</div>
                  <div className="text-xs text-muted-foreground mt-1">{med.dosage_form}</div>
                  <div className="mt-4 flex items-center justify-between">
                    <div className="font-bold text-primary">${Number(med.selling_price).toFixed(2)}</div>
                    <div className={`text-xs px-2 py-1 rounded-full ${med.total_stock > 10 ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'}`}>
                      {med.total_stock} in stock
                    </div>
                  </div>
                </div>
              ))}
              {filteredMedicines.length === 0 && (
                <div className="col-span-full py-12 text-center text-muted-foreground">
                  No medicines found. Try another search term.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Side: Cart & Checkout */}
        <div className="md:col-span-5 lg:col-span-4 flex flex-col border rounded-xl bg-card min-h-0 overflow-hidden shadow-sm">
          <div className="p-4 border-b bg-muted/30 flex justify-between items-center">
            <h3 className="font-semibold flex items-center">
              <ShoppingCart className="h-5 w-5 mr-2 text-primary" />
              Current Order
            </h3>
            <span className="bg-primary text-primary-foreground text-xs px-2 py-1 rounded-full font-medium">
              {items.length} items
            </span>
          </div>

          <div className="flex-1 overflow-auto p-4 space-y-3">
            {fields.map((field, index) => (
              <div key={field.id} className="flex justify-between items-start p-3 border rounded-lg bg-background">
                <div className="flex-1 mr-4">
                  <div className="font-medium text-sm line-clamp-1">{field.medicine_name}</div>
                  <div className="text-xs text-muted-foreground mt-1">${field.unit_price.toFixed(2)} each</div>
                </div>
                
                <div className="flex flex-col items-end">
                  <div className="flex items-center space-x-2 bg-muted rounded-md p-1">
                    <button 
                      type="button"
                      onClick={() => {
                        if (items[index].quantity > 1) {
                          update(index, { ...items[index], quantity: items[index].quantity - 1 });
                        }
                      }}
                      className="p-1 hover:bg-background rounded text-muted-foreground"
                    >
                      <Minus size={14} />
                    </button>
                    <span className="w-6 text-center text-sm font-medium">{items[index].quantity}</span>
                    <button 
                      type="button"
                      onClick={() => {
                        if (items[index].quantity < items[index].max_quantity) {
                          update(index, { ...items[index], quantity: items[index].quantity + 1 });
                        } else {
                          alert("Max stock reached");
                        }
                      }}
                      className="p-1 hover:bg-background rounded text-muted-foreground"
                    >
                      <Plus size={14} />
                    </button>
                  </div>
                  <div className="mt-2 text-sm font-bold">
                    ${(items[index].quantity * items[index].unit_price).toFixed(2)}
                  </div>
                </div>
                
                <button 
                  type="button"
                  onClick={() => remove(index)}
                  className="ml-3 mt-1 text-muted-foreground hover:text-destructive"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            ))}

            {fields.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-muted-foreground py-12">
                <ShoppingCart className="h-12 w-12 mb-4 opacity-20" />
                <p>Cart is empty</p>
                <p className="text-xs mt-1">Scan or search products to add</p>
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="p-4 border-t bg-muted/10">
            <div className="space-y-2 mb-4 text-sm">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tax (5%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between pt-2 border-t">
                <span className="font-semibold text-lg">Total</span>
                <span className="font-bold text-lg text-primary">${total.toFixed(2)}</span>
              </div>
            </div>

            <div className="space-y-4 mb-4">
              <div className="grid grid-cols-4 gap-2">
                {['cash', 'card', 'insurance', 'mobile'].map((method) => (
                  <button
                    key={method}
                    type="button"
                    onClick={() => setValue('payment_method', method as any)}
                    className={`flex flex-col items-center justify-center py-2 rounded-lg border text-xs capitalize ${watch('payment_method') === method ? 'bg-primary text-primary-foreground border-primary' : 'bg-background hover:bg-muted'}`}
                  >
                    {method === 'cash' && <Banknote size={16} className="mb-1" />}
                    {method === 'card' && <CreditCard size={16} className="mb-1" />}
                    {method === 'insurance' && <FileText size={16} className="mb-1" />}
                    {method === 'mobile' && <CreditCard size={16} className="mb-1" />}
                    {method}
                  </button>
                ))}
              </div>

              {watch('payment_method') === 'cash' && (
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1">Amount Tendered ($)</label>
                  <div className="flex items-center gap-2">
                    <button type="button" onClick={() => setValue('amount_paid', total)} className="px-3 py-2 border rounded-md text-xs hover:bg-muted font-medium w-16 text-center">Exact</button>
                    <input 
                      {...register('amount_paid', { valueAsNumber: true })}
                      type="number" 
                      step="0.01"
                      min="0"
                      className="flex-1 px-3 py-2 border rounded-md bg-background focus:ring-1 focus:ring-primary"
                    />
                  </div>
                  {change > 0 && (
                    <div className="mt-2 text-sm flex justify-between text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-950/20 p-2 rounded-md">
                      <span>Change Due:</span>
                      <span className="font-bold">${change.toFixed(2)}</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            <button 
              type="submit" 
              disabled={items.length === 0 || processSale.isPending}
              className="w-full py-4 bg-primary hover:bg-primary/90 text-primary-foreground font-bold rounded-xl shadow-lg transition-all active:scale-[0.98] disabled:opacity-50 disabled:active:scale-100 flex items-center justify-center text-lg"
            >
              {processSale.isPending ? 'Processing...' : 'Pay & Complete'}
            </button>
            {errors.items && <p className="text-destructive text-xs mt-2 text-center">{errors.items.message}</p>}
          </form>
        </div>
      </div>
    </div>
  );
}
