import { TrendingUp } from 'lucide-react';
import { useStore } from '../store';
import { colors, typography } from '../theme/colors';

interface TradingPairSelectorProps {
  pairs: any[];
  selectedSymbol: string;
}

export default function TradingPairSelector({ pairs, selectedSymbol }: TradingPairSelectorProps) {
  const { setSymbol, fiatCurrency, setFiatCurrency } = useStore();

  const selectStyle = {
    width: '100%',
    padding: '12px 16px',
    backgroundColor: colors.background.primary,
    color: colors.text.primary,
    border: `1.5px solid ${colors.border.default}`,
    borderRadius: typography.borderRadius.md,
    fontSize: '1rem',
    fontFamily: typography.fontFamily,
    cursor: 'pointer',
    outline: 'none',
    transition: 'all 0.3s ease',
    boxShadow: colors.shadow.sm,
  };

  const selectFocusStyle = {
    ...selectStyle,
    borderColor: colors.primary.coral,
    boxShadow: `0 0 0 3px ${colors.primary.coral}33, ${colors.shadow.md}`,
  };

  return (
    <div className="section-card">
      <div className="section-title" style={{ color: colors.primary.warmRed }}>
        <TrendingUp />
        Trading Pair Selector
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <label style={{ 
          display: 'block', 
          marginBottom: '10px',
          color: colors.text.primary,
          fontWeight: '600',
          fontSize: '0.95rem'
        }}>
          Select Trading Pair
        </label>
        <select 
          value={selectedSymbol}
          onChange={(e) => setSymbol(e.target.value)}
          style={selectStyle}
          onFocus={(e) => Object.assign(e.target.style, selectFocusStyle)}
          onBlur={(e) => Object.assign(e.target.style, selectStyle)}
        >
          {pairs.map(pair => (
            <option 
              key={pair.symbol} 
              value={pair.symbol}
              style={{
                backgroundColor: colors.background.primary,
                color: colors.text.primary,
                padding: '8px'
              }}
            >
              {pair.symbol} - {pair.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label style={{ 
          display: 'block', 
          marginBottom: '10px',
          color: colors.text.primary,
          fontWeight: '600',
          fontSize: '0.95rem'
        }}>
          Fiat Currency
        </label>
        <select 
          value={fiatCurrency}
          onChange={(e) => setFiatCurrency(e.target.value)}
          style={selectStyle}
          onFocus={(e) => Object.assign(e.target.style, selectFocusStyle)}
          onBlur={(e) => Object.assign(e.target.style, selectStyle)}
        >
          <option 
            value="USD"
            style={{
              backgroundColor: colors.background.primary,
              color: colors.text.primary,
              padding: '8px'
            }}
          >
            USD
          </option>
          <option 
            value="THB"
            style={{
              backgroundColor: colors.background.primary,
              color: colors.text.primary,
              padding: '8px'
            }}
          >
            THB (฿)
          </option>
        </select>
      </div>

      <div style={{
        marginTop: '24px',
        padding: '20px',
        background: `linear-gradient(135deg, ${colors.background.primary} 0%, ${colors.background.secondary} 100%)`,
        border: `1.5px solid ${colors.border.default}`,
        borderRadius: typography.borderRadius.lg,
        boxShadow: colors.shadow.md,
      }}>
        <div style={{ 
          fontSize: '0.85rem', 
          color: colors.text.secondary,
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
          fontWeight: '600',
          marginBottom: '8px'
        }}>
          Selected Pair
        </div>
        <div style={{ 
          fontSize: '1.75rem', 
          fontWeight: 'bold',
          color: colors.primary.warmRed,
          marginBottom: '8px'
        }}>
          {selectedSymbol}
        </div>
        <div style={{ 
          fontSize: '0.9rem', 
          color: colors.text.secondary,
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <span style={{
            display: 'inline-block',
            padding: '4px 12px',
            backgroundColor: colors.primary.sage + '33',
            color: colors.primary.sage,
            borderRadius: typography.borderRadius.round,
            fontSize: '0.85rem',
            fontWeight: '600'
          }}>
            {fiatCurrency}
          </span>
        </div>
      </div>
    </div>
  );
}
