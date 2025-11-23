"""
WebSocket Manager for Real-time Log Push
Broadcasts kill-switch events and critical logs to connected frontend clients
"""
from fastapi import WebSocket
from typing import Dict, Set
import json
import asyncio


class WebSocketManager:
    """Manages WebSocket connections and broadcasts"""
    
    def __init__(self):
        # user_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        async with self._lock:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()
            self.active_connections[user_id].add(websocket)
        print(f"✅ WebSocket connected for user {user_id} (total: {len(self.active_connections[user_id])})")
    
    async def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove a WebSocket connection"""
        async with self._lock:
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
        print(f"❌ WebSocket disconnected for user {user_id}")
    
    async def send_to_user(self, user_id: int, message: dict):
        """Send a message to all connections for a specific user"""
        if user_id not in self.active_connections:
            return
        
        dead_connections = set()
        for connection in self.active_connections[user_id]:
            try:
                # Check if connection is still open before sending
                if connection.client_state.value == 3:  # WebSocketState.CONNECTED
                    await connection.send_json(message)
                else:
                    dead_connections.add(connection)
            except Exception as e:
                print(f"⚠️ Failed to send to WebSocket for user {user_id}: {e}")
                dead_connections.add(connection)
        
        # Clean up dead connections
        if dead_connections:
            async with self._lock:
                self.active_connections[user_id] -= dead_connections
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            print(f"🧹 Cleaned up {len(dead_connections)} dead WebSocket connections for user {user_id}")
    
    async def broadcast_log(self, user_id: int, log_entry: dict):
        """Broadcast a log entry to user's connected clients"""
        print(f"📢 Broadcasting log to user {user_id} (active: {user_id in self.active_connections})")
        message = {
            "type": "log",
            "data": log_entry
        }
        await self.send_to_user(user_id, message)
    
    async def broadcast_kill_switch(self, user_id: int, log_entry: dict):
        """Broadcast a kill-switch event with high priority"""
        message = {
            "type": "kill_switch",
            "data": log_entry,
            "priority": "critical"
        }
        await self.send_to_user(user_id, message)


# Global WebSocket manager instance
ws_manager = WebSocketManager()
