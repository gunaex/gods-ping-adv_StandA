import { useEffect, useState } from 'react';
import { Activity, Target, Brain } from 'lucide-react';
import { botAPI } from '../api';
import { colors, typography } from '../theme/colors';

interface GodsModeMetricsProps {
  symbol: string;
}

export default function GodsModeMetrics({ symbol: _symbol }: GodsModeMetricsProps) {
  const [config, setConfig] = useState<any>(null);

  useEffect(() => {
    loadConfig();
    
    // Auto-refresh every 10 seconds
    const interval = setInterval(loadConfig, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadConfig = async () => {
    try {
      const response = await botAPI.getConfig();
      setConfig(response.data);
    } catch (error) {
      console.error('Failed to load config');
    }
  };

  // Don't show if Gods Mode is not enabled
  if (!config || !config.gods_mode_enabled) {
    return null;
  }

  return (
    <div className="section-card" style={{
      background: `linear-gradient(135deg, ${colors.primary.sage}08 0%, ${colors.primary.coral}08 100%)`,
      border: `2px solid ${colors.primary.warmRed}`,
      boxShadow: `0 4px 20px ${colors.primary.warmRed}30`
    }}>
      <div className="section-title" style={{
        background: `linear-gradient(135deg, ${colors.primary.warmRed} 0%, ${colors.primary.coral} 100%)`,
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        fontWeight: 800
      }}>
        <Brain size={24} />
        GODS MODE - Meta-Model AI Analytics
        <div style={{
          marginLeft: 'auto',
          padding: '6px 16px',
          background: `linear-gradient(135deg, ${colors.primary.warmRed}20 0%, ${colors.primary.coral}20 100%)`,
          border: `2px solid ${colors.primary.warmRed}`,
          borderRadius: typography.borderRadius.round,
          fontSize: '0.85rem',
          fontWeight: 700,
          color: colors.primary.warmRed,
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          boxShadow: `0 0 12px ${colors.primary.warmRed}40`
        }}>
          <Activity size={16} />
          ACTIVE
        </div>
      </div>

      <div style={{
        padding: '24px',
        background: colors.background.card,
        borderRadius: typography.borderRadius.md,
        marginBottom: '20px'
      }}>
        <h3 style={{
          fontSize: '1.1rem',
          color: colors.text.primary,
          marginBottom: '16px',
          fontWeight: 700,
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <Target size={20} color={colors.primary.warmRed} />
          Advanced AI Architecture
        </h3>

        <div className="grid grid-3" style={{ gap: '16px' }}>
          {/* Model A */}
          <div style={{
            padding: '16px',
            background: `linear-gradient(135deg, ${colors.primary.sage}15 0%, ${colors.primary.sage}05 100%)`,
            border: `2px solid ${colors.primary.sage}`,
            borderRadius: typography.borderRadius.md
          }}>
            <div style={{
              fontSize: '0.75rem',
              color: colors.text.secondary,
              marginBottom: '8px',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              Model A
            </div>
            <div style={{
              fontSize: '1.1rem',
              fontWeight: 700,
              color: colors.primary.sage,
              marginBottom: '6px'
            }}>
              📈 Forecaster
            </div>
            <div style={{
              fontSize: '0.85rem',
              color: colors.text.secondary,
              lineHeight: '1.5'
            }}>
              LSTM-inspired price prediction with momentum tracking
            </div>
          </div>

          {/* Model B */}
          <div style={{
            padding: '16px',
            background: `linear-gradient(135deg, ${colors.primary.coral}15 0%, ${colors.primary.coral}05 100%)`,
            border: `2px solid ${colors.primary.coral}`,
            borderRadius: typography.borderRadius.md
          }}>
            <div style={{
              fontSize: '0.75rem',
              color: colors.text.secondary,
              marginBottom: '8px',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              Model B
            </div>
            <div style={{
              fontSize: '1.1rem',
              fontWeight: 700,
              color: colors.primary.coral,
              marginBottom: '6px'
            }}>
              🎯 Classifier
            </div>
            <div style={{
              fontSize: '0.85rem',
              color: colors.text.secondary,
              lineHeight: '1.5'
            }}>
              Regime detection using Parabolic SAR + RSI + Volatility
            </div>
          </div>

          {/* Meta-Model */}
          <div style={{
            padding: '16px',
            background: `linear-gradient(135deg, ${colors.primary.warmRed}15 0%, ${colors.primary.warmRed}05 100%)`,
            border: `2px solid ${colors.primary.warmRed}`,
            borderRadius: typography.borderRadius.md
          }}>
            <div style={{
              fontSize: '0.75rem',
              color: colors.text.secondary,
              marginBottom: '8px',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              Meta-Model
            </div>
            <div style={{
              fontSize: '1.1rem',
              fontWeight: 700,
              color: colors.primary.warmRed,
              marginBottom: '6px'
            }}>
              🧠 Gating Logic
            </div>
            <div style={{
              fontSize: '0.85rem',
              color: colors.text.secondary,
              lineHeight: '1.5'
            }}>
              Ensemble decision tree that gates Models A & B
            </div>
          </div>
        </div>
      </div>

      {/* Strategy Details */}
      <div style={{
        padding: '20px',
        background: `linear-gradient(135deg, ${colors.background.secondary} 0%, ${colors.background.card} 100%)`,
        borderRadius: typography.borderRadius.md,
        border: `1px solid ${colors.border.default}`
      }}>
        <h3 style={{
          fontSize: '1rem',
          color: colors.text.primary,
          marginBottom: '12px',
          fontWeight: 700
        }}>
          🎯 Optimized for Sideways-Down Markets
        </h3>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '12px',
          fontSize: '0.9rem',
          color: colors.text.secondary
        }}>
          <div style={{
            padding: '12px',
            background: colors.background.card,
            borderRadius: typography.borderRadius.sm,
            border: `1px solid ${colors.border.subtle}`
          }}>
            <strong style={{ color: colors.trading.sell.color }}>📉 High Volatility</strong>
            <div style={{ marginTop: '4px', fontSize: '0.85rem' }}>
              Trust Model B regime classifier
            </div>
          </div>

          <div style={{
            padding: '12px',
            background: colors.background.card,
            borderRadius: typography.borderRadius.sm,
            border: `1px solid ${colors.border.subtle}`
          }}>
            <strong style={{ color: colors.trading.neutral.color }}>⚖️ Range-Bound</strong>
            <div style={{ marginTop: '4px', fontSize: '0.85rem' }}>
              Use Model A forecast for entries
            </div>
          </div>

          <div style={{
            padding: '12px',
            background: colors.background.card,
            borderRadius: typography.borderRadius.sm,
            border: `1px solid ${colors.border.subtle}`
          }}>
            <strong style={{ color: colors.primary.sage }}>📊 Strong Trend</strong>
            <div style={{ marginTop: '4px', fontSize: '0.85rem' }}>
              Weighted ensemble of both models
            </div>
          </div>
        </div>
      </div>

      {/* Performance Note */}
      <div style={{
        marginTop: '16px',
        padding: '16px',
        background: `linear-gradient(135deg, ${colors.status.info.bg} 0%, ${colors.background.card} 100%)`,
        borderRadius: typography.borderRadius.md,
        border: `2px solid ${colors.status.info.border}`,
        fontSize: '0.9rem',
        color: colors.text.secondary,
        lineHeight: '1.6'
      }}>
        <strong style={{ color: colors.status.info.color, display: 'block', marginBottom: '8px' }}>
          ⚡ Lightweight & Efficient
        </strong>
         ML training - uses optimized rule-based meta-logic with technical indicators.
      </div>
    </div>
  );
}
