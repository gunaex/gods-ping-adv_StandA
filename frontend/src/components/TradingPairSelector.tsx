import { TrendingUp } from 'lucide-react';
import { useStore } from '../store';

interface TradingPairSelectorProps {
  pairs: any[];
  selectedSymbol: string;
}

export default function TradingPairSelector({ pairs, selectedSymbol }: TradingPairSelectorProps) {
  const { setSymbol, fiatCurrency, setFiatCurrency } = useStore();

  return (
    <div className="section-card">
      <div className="section-title">
        <TrendingUp />
        Trading Pair Selector
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label style={{ display: 'block', marginBottom: '8px' }}>
          Select Trading Pair
        </label>
        <select 
          value={selectedSymbol}
          onChange={(e) => setSymbol(e.target.value)}
          style={{ width: '100%' }}
        >
          {pairs.map(pair => (
            <option key={pair.symbol} value={pair.symbol}>
              {pair.symbol} - {pair.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label style={{ display: 'block', marginBottom: '8px' }}>
          Fiat Currency
        </label>
        <select 
          value={fiatCurrency}
          onChange={(e) => setFiatCurrency(e.target.value)}
          style={{ width: '100%' }}
        >
          <option value="USD">USD</option>
          <option value="THB">THB (฿)</option>
        </select>
      </div>

      <div style={{
        marginTop: '20px',
        padding: '15px',
        background: 'rgba(0, 0, 0, 0.2)',
        borderRadius: '8px',
      }}>
        <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Selected Pair:</div>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{selectedSymbol}</div>
        <div style={{ fontSize: '0.9rem', opacity: 0.8, marginTop: '5px' }}>
          Currency: {fiatCurrency}
        </div>
      </div>
    </div>
  );
}
