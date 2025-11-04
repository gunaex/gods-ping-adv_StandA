import { create } from 'zustand';

interface User {
  id: number;
  username: string;
  is_admin: boolean;
  has_api_keys: boolean;
}

interface AppState {
  user: User | null;
  token: string | null;
  selectedSymbol: string;
  fiatCurrency: string;
  login: (token: string, user: User) => void;
  logout: () => void;
  setSymbol: (symbol: string) => void;
  setFiatCurrency: (currency: string) => void;
}

export const useStore = create<AppState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  selectedSymbol: 'BTC/USDT',
  fiatCurrency: 'USD',
  
  login: (token, user) => {
    localStorage.setItem('token', token);
    set({ token, user });
  },
  
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
  },
  
  setSymbol: (symbol) => set({ selectedSymbol: symbol }),
  
  setFiatCurrency: (currency) => set({ fiatCurrency: currency }),
}));
