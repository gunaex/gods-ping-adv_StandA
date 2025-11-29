import React, { useEffect, useState, useCallback } from 'react';
import api from '../api';

const SystemStatus: React.FC = () => {
  const [status, setStatus] = useState({
    serverOnline: false,
    aiOnline: false,
    message: "Initializing...",
    lastHeartbeat: 0
  });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const checkStatus = useCallback(async () => {
    setIsRefreshing(true);
    try {
      // 1. Check Server Connection (General logs)
      await api.get('/logs?limit=1');
      
      // 2. Check AI Heartbeat specifically (Category: bot)
      // This ensures we find the heartbeat even if other logs are spamming
      const heartbeatRes = await api.get('/logs?category=bot&limit=1');
      const heartbeatLogs = Array.isArray(heartbeatRes.data) ? heartbeatRes.data : (heartbeatRes.data.logs || []);
      
      setStatus(prev => {
        let newAiOnline = false;
        let newMessage = prev.message;
        let newLastHeartbeat = prev.lastHeartbeat;

        // Find the most recent log that contains "Heartbeat"
        const heartbeatLog = heartbeatLogs.find((l: any) => l.message && l.message.includes("Heartbeat"));

        if (heartbeatLog) {
          const heartbeatTime = new Date(heartbeatLog.created_at || heartbeatLog.timestamp).getTime();
          // AI is "Online" if heartbeat is less than 5 minutes old (increased tolerance)
          if (Date.now() - heartbeatTime < 300000) {
            newAiOnline = true;
          }
          newMessage = heartbeatLog.message.replace("❤️ Heartbeat: ", "");
          newLastHeartbeat = heartbeatTime;
        }

        return {
            serverOnline: true,
            aiOnline: newAiOnline,
            message: newMessage,
            lastHeartbeat: newLastHeartbeat
        };
      });

    } catch (error) {
      // Server is unreachable
      setStatus(prev => ({ ...prev, serverOnline: false, aiOnline: false }));
    } finally {
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, [checkStatus]);

  return (
    <div style={{
      position: 'fixed',
      bottom: '15px',
      left: '15px',
      zIndex: 9999,
      background: 'rgba(15, 23, 42, 0.3)', // 30% opacity
      backdropFilter: 'blur(6px)', // Glass effect
      border: '1px solid rgba(51, 65, 85, 0.5)', // Semi-transparent border
      borderRadius: '6px',
      padding: '12px',
      color: '#e2e8f0', // Slate-200
      fontSize: '12px',
      fontFamily: 'monospace',
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3)',
      minWidth: '220px'
    }}>
      {/* Header with Refresh Button */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px', borderBottom: '1px solid #334155', paddingBottom: '4px' }}>
        <span style={{ fontWeight: 'bold', color: '#94a3b8', fontSize: '10px' }}>SYSTEM STATUS</span>
        <button 
            onClick={checkStatus} 
            disabled={isRefreshing}
            style={{
                background: 'transparent',
                border: 'none',
                color: isRefreshing ? '#64748b' : '#38bdf8',
                cursor: isRefreshing ? 'wait' : 'pointer',
                fontSize: '10px',
                padding: '2px 4px',
                textDecoration: 'underline',
                fontFamily: 'monospace'
            }}
        >
            {isRefreshing ? 'REFRESHING...' : 'REFRESH'}
        </button>
      </div>

      {/* Server Status Row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
        <span style={{ opacity: 0.7 }}>SERVER:</span>
        <span style={{ 
            fontWeight: 'bold', 
            color: status.serverOnline ? '#4ade80' : '#f87171' // Light Green : Light Red
        }}>
            {status.serverOnline ? "ONLINE" : "DISCONNECTED"}
        </span>
      </div>

      {/* AI Status Row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
        <span style={{ opacity: 0.7 }}>AI BOT:</span>
        <span style={{ 
            fontWeight: 'bold', 
            color: status.aiOnline ? '#4ade80' : '#fbbf24' // Light Green : Amber (Warning)
        }}>
            {status.aiOnline ? "RUNNING" : "STOPPED"}
        </span>
      </div>

      {/* Heartbeat Message Area */}
      <div style={{ 
          borderTop: '1px solid #334155', 
          paddingTop: '8px',
          fontSize: '11px',
          lineHeight: '1.4'
      }}>
        {status.aiOnline ? (
            <div>
                <div style={{ fontWeight: '600', color: '#fff' }}>{status.message}</div>
                <div style={{ fontSize: '10px', marginTop: '4px', opacity: 0.5 }}>
                    Last signal: {Math.floor((Date.now() - status.lastHeartbeat) / 1000)}s ago
                </div>
            </div>
        ) : (
            <div style={{ fontStyle: 'italic', opacity: 0.6 }}>Waiting for AI signal...</div>
        )}
      </div>
    </div>
  );
};

export default SystemStatus;