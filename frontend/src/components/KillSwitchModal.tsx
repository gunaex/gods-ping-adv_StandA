import { useState } from 'react';
import { AlertTriangle, RefreshCw, X, FileText } from 'lucide-react';
import { colors } from '../theme/colors';
import { API_BASE_URL } from '../api';
import { formatLocalDateTime } from '../utils/timeUtils';

interface KillSwitchDetails {
  unrealized_pl_percent?: number;
  effective_pl_percent?: number;
  baseline_pl_percent?: number | null;
  position_value?: number;
  cost_basis?: number;
  current_price?: number;
  max_daily_loss?: number;
  consecutive_breaches?: number;
  required_breaches?: number;
  cooldown_minutes?: number;
}

interface KillSwitchModalProps {
  logId: number;
  timestamp: string;
  message: string;
  details?: string; // JSON string
  onClose: () => void;
  onOpenLogs?: () => void;
}

export default function KillSwitchModal({ timestamp, message, details, onClose, onOpenLogs }: KillSwitchModalProps) {
  const [loading, setLoading] = useState(false);

  let parsed: KillSwitchDetails | undefined;
  try {
    parsed = details ? JSON.parse(details) : undefined;
  } catch {
    parsed = undefined;
  }

  const handleResetAndContinue = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/bot/gods-hand/reset-kill-switch?restart=true`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text);
      }
      onClose();
    } catch (e) {
      alert('Failed to reset kill-switch baseline. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0, 0, 0, 0.75)', backdropFilter: 'blur(4px)',
      display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1100, padding: 20
    }}>
      <div style={{
        width: '95%', maxWidth: 720,
        background: 'linear-gradient(135deg, #1f2937 0%, #0b1220 100%)',
        border: '1px solid rgba(255,255,255,0.1)', borderRadius: 14, color: '#fff'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 18px', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <AlertTriangle size={22} style={{ color: colors.status.error.color }} />
            <strong>Kill-Switch Triggered</strong>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer' }}>
            <X size={20} />
          </button>
        </div>

        <div style={{ padding: 18 }}>
          <div style={{ opacity: 0.8, fontSize: '0.9rem', marginBottom: 10 }}>{formatLocalDateTime(timestamp)}</div>
          <div style={{ fontSize: '1rem', marginBottom: 12, color: colors.status.error.color }}>{message}</div>

          {parsed && (
            <div style={{
              display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12,
              background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.1)', padding: 12, borderRadius: 8, marginBottom: 12
            }}>
              <div>Unrealized P/L: <strong style={{ color: colors.status.error.color }}>{parsed.unrealized_pl_percent?.toFixed(2)}%</strong></div>
              {parsed.effective_pl_percent !== undefined && (
                <div>Effective P/L vs baseline: <strong>{parsed.effective_pl_percent?.toFixed(2)}%</strong></div>
              )}
              <div>Baseline P/L: <strong>{parsed.baseline_pl_percent !== undefined && parsed.baseline_pl_percent !== null ? `${parsed.baseline_pl_percent.toFixed(2)}%` : '—'}</strong></div>
              <div>Max Loss Limit: <strong>-{parsed.max_daily_loss}%</strong></div>
              {parsed.consecutive_breaches !== undefined && (
                <div>Consecutive Breaches: <strong>{parsed.consecutive_breaches}/{parsed.required_breaches || '?'}</strong></div>
              )}
              <div>Position Value: <strong>${parsed.position_value?.toFixed(2)}</strong></div>
              <div>Cost Basis: <strong>${parsed.cost_basis?.toFixed(2)}</strong></div>
              <div>Current Price: <strong>${parsed.current_price?.toFixed(4)}</strong></div>
            </div>
          )}

          <div style={{
            padding: 12, marginBottom: 12,
            background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: 8,
            fontSize: '0.9rem', lineHeight: 1.4
          }}>
            <strong>What happens next:</strong>
            <ul style={{ marginTop: 6, marginBottom: 0, paddingLeft: 20 }}>
              <li>Gods Hand is now paused to prevent further losses</li>
              <li>Trading will remain paused for {parsed?.cooldown_minutes || 60} minutes (cooldown period)</li>
              <li>Click "Continue & Reset Baseline" to set a new baseline and restart immediately</li>
              <li>Or wait for the cooldown to expire and manually restart later</li>
            </ul>
          </div>

          <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
            <button onClick={onOpenLogs} style={{
              padding: '8px 14px', borderRadius: 8, cursor: 'pointer',
              background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.15)', color: '#fff'
            }}>
              <FileText size={16} style={{ marginRight: 6, verticalAlign: 'middle' }} /> View Logs
            </button>
            <button onClick={handleResetAndContinue} disabled={loading} style={{
              padding: '8px 14px', borderRadius: 8, cursor: 'pointer',
              background: colors.status.warning.bg, border: `1px solid ${colors.status.warning.border}`, color: colors.status.warning.color,
              display: 'flex', alignItems: 'center', gap: 6
            }}>
              <RefreshCw size={16} /> {loading ? 'Resetting...' : 'Continue & Reset Baseline'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
