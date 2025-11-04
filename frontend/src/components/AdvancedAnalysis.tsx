import { useEffect, useState } from 'react';
import { Activity, RefreshCw } from 'lucide-react';
import { aiAPI } from '../api';

interface AdvancedAnalysisProps {
  symbol: string;
}

export default function AdvancedAnalysis({ symbol }: AdvancedAnalysisProps) {
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadAnalysis();
  }, [symbol]);

  const loadAnalysis = async () => {
    setLoading(true);
    try {
      const response = await aiAPI.getAnalysis(symbol);
      setAnalysis(response.data);
    } catch (error) {
      console.error('Failed to load analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section-card">
      <div className="section-title">
        <Activity />
        Advanced AI Analysis
        <button 
          onClick={loadAnalysis} 
          disabled={loading}
          style={{ marginLeft: 'auto', padding: '5px 15px' }}
        >
          <RefreshCw size={16} />
        </button>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          Analyzing market...
        </div>
      ) : analysis && !analysis.error ? (
        <div>
          {/* Trends */}
          <div style={{ marginBottom: '15px' }}>
            <div style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '10px' }}>
              Multi-Timeframe Trends
            </div>
            <div className="grid grid-3">
              {['1h', '4h', '1d'].map(tf => (
                <div key={tf} style={{
                  padding: '10px',
                  background: 'rgba(0, 0, 0, 0.2)',
                  borderRadius: '8px',
                  textAlign: 'center',
                }}>
                  <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>{tf}</div>
                  <div style={{
                    fontSize: '1.1rem',
                    fontWeight: 'bold',
                    color: analysis.trends[tf] === 'UPTREND' ? '#4ade80' :
                           analysis.trends[tf] === 'DOWNTREND' ? '#f87171' : '#fbbf24',
                  }}>
                    {analysis.trends[tf]}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Support/Resistance */}
          {analysis.levels && (
            <div style={{ marginBottom: '15px' }}>
              <div style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '10px' }}>
                Key Levels
              </div>
              <div className="grid grid-3">
                <div style={{
                  padding: '10px',
                  background: 'rgba(0, 0, 0, 0.2)',
                  borderRadius: '8px',
                }}>
                  <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Support</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#4ade80' }}>
                    ${analysis.levels.support?.toFixed(2)}
                  </div>
                </div>
                <div style={{
                  padding: '10px',
                  background: 'rgba(0, 0, 0, 0.2)',
                  borderRadius: '8px',
                }}>
                  <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Current</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
                    ${analysis.levels.current?.toFixed(2)}
                  </div>
                </div>
                <div style={{
                  padding: '10px',
                  background: 'rgba(0, 0, 0, 0.2)',
                  borderRadius: '8px',
                }}>
                  <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Resistance</div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#f87171' }}>
                    ${analysis.levels.resistance?.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Volatility */}
          <div style={{
            padding: '10px',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
          }}>
            <span style={{ opacity: 0.8 }}>Volatility:</span>
            <span style={{ marginLeft: '10px', fontSize: '1.1rem', fontWeight: 'bold' }}>
              {analysis.volatility?.toFixed(2)}%
            </span>
          </div>
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px', opacity: 0.6 }}>
          No analysis available
        </div>
      )}
    </div>
  );
}
