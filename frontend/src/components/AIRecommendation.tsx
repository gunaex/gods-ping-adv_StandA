import { useEffect, useState } from 'react';
import { Lightbulb, RefreshCw } from 'lucide-react';
import { aiAPI } from '../api';

interface AIRecommendationProps {
  symbol: string;
}

export default function AIRecommendation({ symbol }: AIRecommendationProps) {
  const [recommendation, setRecommendation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadRecommendation();
  }, [symbol]);

  const loadRecommendation = async () => {
    setLoading(true);
    try {
      const response = await aiAPI.getRecommendation(symbol);
      setRecommendation(response.data);
    } catch (error) {
      console.error('Failed to load recommendation:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'BUY': return '#4ade80';
      case 'SELL': return '#f87171';
      default: return '#fbbf24';
    }
  };

  return (
    <div className="section-card">
      <div className="section-title">
        <Lightbulb />
        AI Recommendation
        <button 
          onClick={loadRecommendation} 
          disabled={loading}
          style={{ marginLeft: 'auto', padding: '5px 15px' }}
        >
          <RefreshCw size={16} />
        </button>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          Loading recommendation...
        </div>
      ) : recommendation ? (
        <div>
          <div style={{
            padding: '20px',
            background: `linear-gradient(135deg, ${getActionColor(recommendation.action)}22, ${getActionColor(recommendation.action)}11)`,
            borderRadius: '8px',
            border: `2px solid ${getActionColor(recommendation.action)}`,
            marginBottom: '15px',
          }}>
            <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Action</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: getActionColor(recommendation.action) }}>
              {recommendation.action}
            </div>
          </div>

          <div style={{
            padding: '15px',
            background: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
            marginBottom: '15px',
          }}>
            <div style={{ marginBottom: '10px' }}>
              <span style={{ opacity: 0.8 }}>Confidence:</span>
              <span style={{ marginLeft: '10px', fontSize: '1.2rem', fontWeight: 'bold' }}>
                {(recommendation.confidence * 100).toFixed(0)}%
              </span>
            </div>
            <div style={{
              width: '100%',
              height: '8px',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '4px',
              overflow: 'hidden',
            }}>
              <div style={{
                width: `${recommendation.confidence * 100}%`,
                height: '100%',
                background: getActionColor(recommendation.action),
              }} />
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.9rem', opacity: 0.8, marginBottom: '10px' }}>
              Reasoning:
            </div>
            {recommendation.reasoning && recommendation.reasoning.map((reason: string, i: number) => (
              <div key={i} style={{
                padding: '8px',
                background: 'rgba(0, 0, 0, 0.2)',
                borderRadius: '4px',
                marginBottom: '5px',
                fontSize: '0.9rem',
              }}>
                • {reason}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '40px', opacity: 0.6 }}>
          No recommendation available
        </div>
      )}
    </div>
  );
}
