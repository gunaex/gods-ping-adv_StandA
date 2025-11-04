import { useEffect, useState } from 'react';
import { 
  LogOut, Settings, TrendingUp, BarChart3, Bot, 
  Zap, Activity, DollarSign 
} from 'lucide-react';
import { useStore } from '../store';
import { tradingAPI, marketAPI, aiAPI, botAPI } from '../api';
import TradingPairSelector from './TradingPairSelector';
import AIRecommendation from './AIRecommendation';
import MarketData from './MarketData';
import BotsPanel from './BotsPanel';
import AdvancedAnalysis from './AdvancedAnalysis';
import GodsHand from './GodsHand';
import SettingsModal from './SettingsModal';

export default function ShichiFukujin() {
  const { user, logout, selectedSymbol, fiatCurrency } = useStore();
  const [showSettings, setShowSettings] = useState(false);
  const [tradingPairs, setTradingPairs] = useState<any[]>([]);

  useEffect(() => {
    loadTradingPairs();
  }, []);

  const loadTradingPairs = async () => {
    try {
      const response = await tradingAPI.getPairs();
      setTradingPairs(response.data.pairs);
    } catch (error) {
      console.error('Failed to load trading pairs:', error);
    }
  };

  return (
    <div className="container">
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px',
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        padding: '20px',
        borderRadius: '12px',
        border: '1px solid rgba(255, 255, 255, 0.2)',
      }}>
        <div>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '5px' }}>
            Gods Ping
          </h1>
          <p style={{ opacity: 0.8 }}>七福神 Shichi-Fukujin Trading Platform</p>
        </div>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ opacity: 0.8 }}>Welcome, {user?.username}</span>
          <button onClick={() => setShowSettings(true)}>
            <Settings size={20} />
            Settings
          </button>
          <button onClick={logout}>
            <LogOut size={20} />
            Logout
          </button>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-2">
        {/* Section 1: Trading Pair Selector */}
        <TradingPairSelector 
          pairs={tradingPairs} 
          selectedSymbol={selectedSymbol}
        />

        {/* Section 2: AI Recommendation */}
        <AIRecommendation symbol={selectedSymbol} />
      </div>

      {/* Section 3: Market Data & Chart */}
      <MarketData symbol={selectedSymbol} fiatCurrency={fiatCurrency} />

      <div className="grid grid-2">
        {/* Section 4: Grid Bot & DCA Bot */}
        <BotsPanel />

        {/* Section 5: Advanced AI Analysis */}
        <AdvancedAnalysis symbol={selectedSymbol} />
      </div>

      {/* Section 6: Gods Hand */}
      <GodsHand symbol={selectedSymbol} />

      {/* Settings Modal */}
      {showSettings && (
        <SettingsModal onClose={() => setShowSettings(false)} />
      )}
    </div>
  );
}
