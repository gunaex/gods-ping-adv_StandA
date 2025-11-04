import { useState } from 'react';
import { Bot, Grid, DollarSign, Play, StopCircle } from 'lucide-react';
import { botAPI } from '../api';

export default function BotsPanel() {
  const [gridConfig, setGridConfig] = useState({
    lowerPrice: '',
    upperPrice: '',
    levels: '10',
  });
  const [dcaConfig, setDcaConfig] = useState({
    amount: '',
    interval: '1',
  });
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const startGridBot = async () => {
    setLoading(true);
    try {
      // First update config
      await botAPI.updateConfig({
        grid_enabled: true,
        grid_lower_price: parseFloat(gridConfig.lowerPrice),
        grid_upper_price: parseFloat(gridConfig.upperPrice),
        grid_levels: parseInt(gridConfig.levels),
      });
      
      // Then start bot
      const response = await botAPI.startGrid();
      alert(response.data.message);
      loadStatus();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to start Grid Bot');
    } finally {
      setLoading(false);
    }
  };

  const startDCABot = async () => {
    setLoading(true);
    try {
      await botAPI.updateConfig({
        dca_enabled: true,
        dca_amount_per_period: parseFloat(dcaConfig.amount),
        dca_interval_days: parseInt(dcaConfig.interval),
      });
      
      const response = await botAPI.startDCA();
      alert(response.data.message);
      loadStatus();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to start DCA Bot');
    } finally {
      setLoading(false);
    }
  };

  const stopBot = async (botType: string) => {
    try {
      const response = await botAPI.stopBot(botType);
      alert(response.data.message);
      loadStatus();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to stop bot');
    }
  };

  const loadStatus = async () => {
    try {
      const response = await botAPI.getStatus();
      setStatus(response.data);
    } catch (error) {
      console.error('Failed to load status');
    }
  };

  return (
    <div className="section-card">
      <div className="section-title">
        <Bot />
        Trading Bots
      </div>

      {/* Grid Bot */}
      <div style={{ marginBottom: '20px', padding: '15px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}>
          <Grid size={20} />
          Grid Bot
        </h3>

        <div className="grid grid-3" style={{ marginBottom: '10px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '5px' }}>
              Lower Price
            </label>
            <input
              type="number"
              value={gridConfig.lowerPrice}
              onChange={(e) => setGridConfig({...gridConfig, lowerPrice: e.target.value})}
              placeholder="40000"
              style={{ width: '100%' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '5px' }}>
              Upper Price
            </label>
            <input
              type="number"
              value={gridConfig.upperPrice}
              onChange={(e) => setGridConfig({...gridConfig, upperPrice: e.target.value})}
              placeholder="50000"
              style={{ width: '100%' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '5px' }}>
              Levels
            </label>
            <input
              type="number"
              value={gridConfig.levels}
              onChange={(e) => setGridConfig({...gridConfig, levels: e.target.value})}
              placeholder="10"
              style={{ width: '100%' }}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={startGridBot} disabled={loading}>
            <Play size={16} />
            Start Grid
          </button>
          <button onClick={() => stopBot('grid')}>
            <StopCircle size={16} />
            Stop
          </button>
        </div>
      </div>

      {/* DCA Bot */}
      <div style={{ padding: '15px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}>
          <DollarSign size={20} />
          DCA Bot
        </h3>

        <div className="grid grid-2" style={{ marginBottom: '10px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '5px' }}>
              Amount per Period ($)
            </label>
            <input
              type="number"
              value={dcaConfig.amount}
              onChange={(e) => setDcaConfig({...dcaConfig, amount: e.target.value})}
              placeholder="100"
              style={{ width: '100%' }}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.9rem', marginBottom: '5px' }}>
              Interval (days)
            </label>
            <input
              type="number"
              value={dcaConfig.interval}
              onChange={(e) => setDcaConfig({...dcaConfig, interval: e.target.value})}
              placeholder="1"
              style={{ width: '100%' }}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={startDCABot} disabled={loading}>
            <Play size={16} />
            Start DCA
          </button>
          <button onClick={() => stopBot('dca')}>
            <StopCircle size={16} />
            Stop
          </button>
        </div>
      </div>

      {status && (
        <div style={{ marginTop: '15px', padding: '10px', background: 'rgba(0, 0, 0, 0.3)', borderRadius: '8px' }}>
          <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>
            Grid: <span style={{ color: status.grid === 'running' ? '#4ade80' : '#fbbf24' }}>
              {status.grid}
            </span> | 
            DCA: <span style={{ color: status.dca === 'running' ? '#4ade80' : '#fbbf24' }}>
              {status.dca}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
