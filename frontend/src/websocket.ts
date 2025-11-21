/**
 * WebSocket connection manager for real-time log updates
 */

import { API_BASE_URL } from './api';

type MessageHandler = (message: any) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private reconnectTimer: number | null = null;
  private token: string | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private connected: boolean = false;

  connect(token: string) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return; // Already connected
    }

    this.token = token;
    
    // Build WebSocket URL - handle development vs production
    let wsUrl: string;
    if (import.meta.env.DEV) {
      // Development: use Vite proxy (ws://localhost:5173/ws proxies to ws://localhost:8000/ws)
      wsUrl = `ws://${window.location.host}`;
    } else {
      // Production: use the API base URL but replace http/https with ws/wss
      wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://').replace('/api', '');
    }
    const url = `${wsUrl}/ws/logs/${token}`;

    console.log('🔌 Attempting WebSocket connection:', url);
    
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('✅ WebSocket connected successfully');
      this.connected = true;
      this.reconnectAttempts = 0; // Reset attempts on successful connection
      
      if (this.reconnectTimer) {
        clearTimeout(this.reconnectTimer);
        this.reconnectTimer = null;
      }
      
      // Start ping/pong to keep connection alive
      this.startPing();
    };

    this.ws.onmessage = (event) => {
      // Handle ping/pong messages (plain text)
      if (event.data === 'pong' || event.data === 'ping') {
        console.log(`🏓 Received ${event.data}`);
        return;
      }
      
      // Handle JSON messages
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e, 'Data:', event.data);
      }
    };

    this.ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error);
    };

    this.ws.onclose = (event) => {
      console.log('🔌 WebSocket disconnected:', event.code, event.reason);
      this.ws = null;
      this.connected = false;
      
      // Auto-reconnect with exponential backoff if we haven't exceeded max attempts
      if (this.token && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        const backoffTime = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000); // Cap at 30s
        
        console.log(`🔄 Reconnecting WebSocket in ${backoffTime}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
        
        this.reconnectTimer = window.setTimeout(() => {
          this.connect(this.token!);
        }, backoffTime);
      } else if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.warn('⚠️ WebSocket max reconnection attempts reached. Giving up.');
      }
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    this.token = null;
    this.connected = false;
    this.reconnectAttempts = 0;
  }

  isConnected(): boolean {
    return this.connected && this.ws?.readyState === WebSocket.OPEN;
  }

  private startPing() {
    const pingInterval = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send('ping');
      } else {
        clearInterval(pingInterval);
      }
    }, 30000); // Ping every 30 seconds
  }

  private handleMessage(message: any) {
    const { type } = message;
    const handlers = this.handlers.get(type);
    
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message);
        } catch (e) {
          console.error(`Error in ${type} handler:`, e);
        }
      });
    }
    
    // Also notify 'all' handlers
    const allHandlers = this.handlers.get('all');
    if (allHandlers) {
      allHandlers.forEach(handler => {
        try {
          handler(message);
        } catch (e) {
          console.error('Error in all handler:', e);
        }
      });
    }
  }

  on(type: string, handler: MessageHandler) {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)!.add(handler);
  }

  off(type: string, handler: MessageHandler) {
    const handlers = this.handlers.get(type);
    if (handlers) {
      handlers.delete(handler);
    }
  }
}

export const wsClient = new WebSocketClient();
