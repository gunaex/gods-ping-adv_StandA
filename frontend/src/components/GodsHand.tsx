import { useState, useEffect } from 'react';
import { Zap, Play, StopCircle, AlertTriangle, Shield, DollarSign } from 'lucide-react';
import { botAPI } from '../api';

interface GodsHandProps {
  symbol: string;
}

export default function GodsHand({ symbol }: GodsHandProps) {
  const [config, setConfig] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadConfig();
    loadStatus();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await botAPI.getConfig();
      setConfig(response.data);
    } catch (error) {
      console.error('Failed to load config');
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

  const startGodsHand = async () => {
    setLoading(true);
    try {
      await botAPI.updateConfig({ gods_hand_enabled: true });
      const response = await botAPI.startGodsHand();
      setResult(response.data);
      loadStatus();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to start Gods Hand');
    } finally {
      setLoading(false);
    }
  };

  const stopGodsHand = async () => {
    try {
      const response = await botAPI.stopBot('gods-hand');
      alert(response.data.message);
      loadStatus();
      setResult(null);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to stop Gods Hand');
    }
  };

  return (
    <div className="section-card">
      <div className="section-title">
        <Zap />
        Gods Hand - AI Autonomous Trading
      </div>

      <div className="grid grid-2" style={{ marginBottom: '20px' }}>
        {/* Current Config */}
        {config && (
          <div style={{ padding: '15px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px' }}>
            <h3 style={{ marginBottom: '10px', fontSize: '1.1rem' }}>Current Configuration</h3>
            <div style={{ fontSize: '0.9rem', lineHeight: '1.8' }}>
              <div>Symbol: <strong>{config.symbol}</strong></div>
              <div>Budget: <strong>${config.budget}</strong></div>
              <div>Risk Level: <strong>{config.risk_level}</strong></div>
              <div>Min Confidence: <strong>{(config.min_confidence * 100).toFixed(0)}%</strong></div>
              <div>Paper Trading: <strong style={{ color: config.paper_trading ? '#4ade80' : '#f87171' }}>
                {config.paper_trading ? 'ON' : 'OFF'}
              </strong></div>
            </div>
          </div>
        )}

        {/* Risk Assessment */}
        {result?.risk_assessment && (
          <div style={{ padding: '15px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px' }}>
            <h3 style={{ marginBottom: '10px', fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Shield size={18} />
              Risk Assessment
            </h3>
            <div style={{ fontSize: '0.9rem', lineHeight: '1.8' }}>
              <div>Risk Score: <strong>{result.risk_assessment.risk_score}/100</strong></div>
              <div>Volatility: <strong>{result.risk_assessment.volatility}%</strong></div>
              <div>Position Size: <strong>${result.risk_assessment.recommended_position_size}</strong></div>
            </div>
          </div>
        )}

        {/* Fee Protection */}
        {result?.risk_assessment && (
          <div style={{ padding: '15px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px' }}>
            <h3 style={{ marginBottom: '10px', fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <DollarSign size={18} />
              Fee Protection
            </h3>
            <div style={{ fontSize: '0.9rem', lineHeight: '1.8' }}>
              <div>Estimated Fees: <strong>${result.risk_assessment.estimated_fees?.toFixed(2)}</strong></div>
              <div>Max Daily Loss: <strong>{result.risk_assessment.max_daily_loss}%</strong></div>
            </div>
          </div>
        )}

        {/* Last Result */}
        {result && (
          <div style={{ padding: '15px', background: 'rgba(0, 0, 0, 0.2)', borderRadius: '8px' }}>
            <h3 style={{ marginBottom: '10px', fontSize: '1.1rem' }}>Last Action</h3>
            <div style={{
              padding: '15px',
              background: result.action === 'HOLD' ? 'rgba(251, 191, 36, 0.1)' :
                         result.action === 'BUY' ? 'rgba(74, 222, 128, 0.1)' :
                         'rgba(248, 113, 113, 0.1)',
              borderRadius: '8px',
              border: `2px solid ${
                result.action === 'HOLD' ? '#fbbf24' :
                result.action === 'BUY' ? '#4ade80' : '#f87171'
              }`,
            }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                {result.action}
              </div>
              <div style={{ fontSize: '0.9rem', opacity: 0.8, marginTop: '5px' }}>
                Confidence: {(result.confidence * 100).toFixed(0)}%
              </div>
              <div style={{ fontSize: '0.9rem', marginTop: '10px' }}>
                {result.message}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Controls */}
      <div style={{
        padding: '20px',
        background: 'rgba(0, 0, 0, 0.3)',
        borderRadius: '8px',
        display: 'flex',
        gap: '10px',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            background: status?.gods_hand === 'running' ? '#4ade80' : '#6b7280',
          }} />
          <span style={{ fontSize: '0.9rem', opacity: 0.8 }}>
            Status: {status?.gods_hand || 'stopped'}
          </span>
        </div>

        <div style={{ display: 'flex', gap: '10px' }}>
          <button onClick={startGodsHand} disabled={loading || status?.gods_hand === 'running'}>
            <Play size={16} />
            Execute Now
          </button>
          <button onClick={stopGodsHand} disabled={status?.gods_hand !== 'running'}>
            <StopCircle size={16} />
            Stop
          </button>
        </div>
      </div>

      {config?.paper_trading && (
        <div style={{
          marginTop: '15px',
          padding: '10px',
          background: 'rgba(251, 191, 36, 0.1)',
          borderRadius: '8px',
          border: '1px solid #fbbf24',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
        }}>
          <AlertTriangle size={16} color="#fbbf24" />
          <span style={{ fontSize: '0.9rem' }}>
            Paper Trading Mode Active - No real trades will be executed
          </span>
        </div>
      )}
    </div>
  );
}
