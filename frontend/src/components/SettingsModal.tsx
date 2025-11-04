import { useState, useEffect } from 'react';
import { X, Save } from 'lucide-react';
import { botAPI, settingsAPI, authAPI } from '../api';
import { useStore } from '../store';

interface SettingsModalProps {
  onClose: () => void;
}

export default function SettingsModal({ onClose }: SettingsModalProps) {
  const { user } = useStore();
  const [config, setConfig] = useState<any>(null);
  const [apiKeys, setApiKeys] = useState({ api_key: '', api_secret: '' });
  const [newUser, setNewUser] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await botAPI.getConfig();
      setConfig(response.data);
    } catch (error) {
      console.error('Failed to load config');
    }
  };

  const saveConfig = async () => {
    setLoading(true);
    try {
      await botAPI.updateConfig(config);
      alert('Settings saved successfully!');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to save settings');
    } finally {
      setLoading(false);
    }
  };

  const saveAPIKeys = async () => {
    setLoading(true);
    try {
      await settingsAPI.updateAPIKeys(apiKeys.api_key, apiKeys.api_secret);
      alert('API keys saved successfully!');
      setApiKeys({ api_key: '', api_secret: '' });
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to save API keys');
    } finally {
      setLoading(false);
    }
  };

  const createUser = async () => {
    setLoading(true);
    try {
      await authAPI.createUser(newUser.username, newUser.password);
      alert('User created successfully!');
      setNewUser({ username: '', password: '' });
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to create user');
    } finally {
      setLoading(false);
    }
  };

  if (!config) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ fontSize: '1.8rem' }}>Settings</h2>
          <button onClick={onClose} style={{ padding: '5px 10px' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ maxHeight: '70vh', overflowY: 'auto' }}>
          {/* Trading Settings */}
          <div style={{ marginBottom: '25px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '15px' }}>Trading Settings</h3>
            
            <div className="grid grid-2" style={{ marginBottom: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Trading Symbol
                </label>
                <select
                  value={config.symbol}
                  onChange={(e) => setConfig({...config, symbol: e.target.value})}
                  style={{ width: '100%' }}
                >
                  <option value="BTC/USDT">BTC/USDT</option>
                  <option value="ETH/USDT">ETH/USDT</option>
                  <option value="BNB/USDT">BNB/USDT</option>
                  <option value="SOL/USDT">SOL/USDT</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Fiat Currency
                </label>
                <select
                  value={config.fiat_currency}
                  onChange={(e) => setConfig({...config, fiat_currency: e.target.value})}
                  style={{ width: '100%' }}
                >
                  <option value="USD">USD</option>
                  <option value="THB">THB (฿)</option>
                </select>
              </div>
            </div>

            <div className="grid grid-2" style={{ marginBottom: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Budget ($)
                </label>
                <input
                  type="number"
                  value={config.budget}
                  onChange={(e) => setConfig({...config, budget: parseFloat(e.target.value)})}
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Paper Trading
                </label>
                <select
                  value={config.paper_trading ? 'true' : 'false'}
                  onChange={(e) => setConfig({...config, paper_trading: e.target.value === 'true'})}
                  style={{ width: '100%' }}
                >
                  <option value="true">ON (Recommended)</option>
                  <option value="false">OFF (Live Trading)</option>
                </select>
              </div>
            </div>
          </div>

          {/* Risk Management */}
          <div style={{ marginBottom: '25px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '15px' }}>Risk Management</h3>
            
            <div className="grid grid-3" style={{ marginBottom: '15px' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Risk Level
                </label>
                <select
                  value={config.risk_level}
                  onChange={(e) => setConfig({...config, risk_level: e.target.value})}
                  style={{ width: '100%' }}
                >
                  <option value="conservative">Conservative</option>
                  <option value="moderate">Moderate</option>
                  <option value="aggressive">Aggressive</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Min Confidence (%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={(config.min_confidence * 100).toFixed(0)}
                  onChange={(e) => setConfig({...config, min_confidence: parseFloat(e.target.value) / 100})}
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Max Daily Loss (%)
                </label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={config.max_daily_loss}
                  onChange={(e) => setConfig({...config, max_daily_loss: parseFloat(e.target.value)})}
                  style={{ width: '100%' }}
                />
              </div>
            </div>
          </div>

          {/* API Keys */}
          <div style={{ marginBottom: '25px' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '15px' }}>Binance API Keys</h3>
            
            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                API Key
              </label>
              <input
                type="text"
                value={apiKeys.api_key}
                onChange={(e) => setApiKeys({...apiKeys, api_key: e.target.value})}
                placeholder="Enter your Binance API Key"
                style={{ width: '100%' }}
              />
            </div>

            <div style={{ marginBottom: '15px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                API Secret
              </label>
              <input
                type="password"
                value={apiKeys.api_secret}
                onChange={(e) => setApiKeys({...apiKeys, api_secret: e.target.value})}
                placeholder="Enter your Binance API Secret"
                style={{ width: '100%' }}
              />
            </div>

            <button onClick={saveAPIKeys} disabled={loading || !apiKeys.api_key || !apiKeys.api_secret}>
              <Save size={16} />
              Save API Keys
            </button>
          </div>

          {/* Create User (Admin Only) */}
          {user?.is_admin && (
            <div style={{ marginBottom: '25px' }}>
              <h3 style={{ fontSize: '1.2rem', marginBottom: '15px' }}>Create Additional User</h3>
              
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Username
                </label>
                <input
                  type="text"
                  value={newUser.username}
                  onChange={(e) => setNewUser({...newUser, username: e.target.value})}
                  placeholder="New username"
                  style={{ width: '100%' }}
                />
              </div>

              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', fontSize: '0.9rem' }}>
                  Password
                </label>
                <input
                  type="password"
                  value={newUser.password}
                  onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                  placeholder="New password"
                  style={{ width: '100%' }}
                />
              </div>

              <button onClick={createUser} disabled={loading || !newUser.username || !newUser.password}>
                Create User
              </button>
            </div>
          )}
        </div>

        {/* Save Button */}
        <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid rgba(255, 255, 255, 0.2)' }}>
          <button onClick={saveConfig} disabled={loading} style={{ width: '100%' }}>
            <Save size={20} />
            Save All Settings
          </button>
        </div>
      </div>
    </div>
  );
}
