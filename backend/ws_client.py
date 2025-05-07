"""
ws_client.py

This module provides a WebSocket client to connect to a cloud server and receive commands.
"""

import asyncio
import json
import logging
import threading
import websockets
from typing import Optional, Dict, Any, Callable
from websockets.exceptions import ConnectionClosed

from routine_state import routine_state

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketClient:
    """
    A WebSocket client that connects to a cloud server and receives commands.
    """
    
    def __init__(self, server_url: str, reconnect_interval: int = 5):
        """
        Initialize the WebSocket client.
        
        Args:
            server_url: URL of the WebSocket server
            reconnect_interval: Interval in seconds to attempt reconnection
        """
        self.server_url = server_url
        self.reconnect_interval = reconnect_interval
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False
        self.connected = False
        self._lock = threading.Lock()
        
        # Command handlers
        self.command_handlers = {
            "start_routine": self._handle_start_routine,
            "next_task": self._handle_next_task,
            "stop_routine": self._handle_stop_routine,
            "play_sound": self._handle_play_sound,
        }
    
    async def connect(self):
        """Connect to the WebSocket server."""
        logger.info(f"Connecting to WebSocket server at {self.server_url}")
        try:
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            logger.info("Connected to WebSocket server")
            
            # Send initial status
            await self._send_status()
            
            return True
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket server: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.connected = False
            logger.info("Disconnected from WebSocket server")
    
    async def _send_message(self, message: Dict[str, Any]):
        """
        Send a message to the WebSocket server.
        
        Args:
            message: Message to send
        """
        if not self.connected or not self.websocket:
            logger.warning("Cannot send message: not connected")
            return
        
        try:
            await self.websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self.connected = False
    
    async def _send_status(self):
        """Send the current status to the WebSocket server."""
        status = {
            "type": "status",
            "data": {
                "is_active": routine_state.is_routine_active,
                "current_task": routine_state.current_task,
                "current_sound": routine_state.current_sound
            }
        }
        await self._send_message(status)
    
    async def _handle_message(self, message_str: str):
        """
        Handle a message received from the WebSocket server.
        
        Args:
            message_str: JSON message string
        """
        try:
            message = json.loads(message_str)
            
            # Check if the message is a command
            if "type" in message and message["type"] == "command":
                command = message.get("command")
                data = message.get("data", {})
                
                if command in self.command_handlers:
                    # Handle the command
                    await self.command_handlers[command](data)
                    
                    # Send updated status after handling command
                    await self._send_status()
                else:
                    logger.warning(f"Unknown command: {command}")
            
        except json.JSONDecodeError:
            logger.error(f"Failed to parse message: {message_str}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _handle_start_routine(self, data: Dict[str, Any]):
        """
        Handle the start_routine command.
        
        Args:
            data: Command data
        """
        logger.info("Received command: start_routine")
        routine_state.start_routine()
    
    async def _handle_next_task(self, data: Dict[str, Any]):
        """
        Handle the next_task command.
        
        Args:
            data: Command data
        """
        logger.info("Received command: next_task")
        routine_state.next_task()
    
    async def _handle_stop_routine(self, data: Dict[str, Any]):
        """
        Handle the stop_routine command.
        
        Args:
            data: Command data
        """
        logger.info("Received command: stop_routine")
        routine_state.stop_routine()
    
    async def _handle_play_sound(self, data: Dict[str, Any]):
        """
        Handle the play_sound command.
        
        Args:
            data: Command data
        """
        sound_name = data.get("sound_name")
        if sound_name:
            logger.info(f"Received command: play_sound {sound_name}")
            routine_state.play_sound(sound_name)
        else:
            logger.warning("Received play_sound command without sound_name")
    
    async def _receive_messages(self):
        """Receive and handle messages from the WebSocket server."""
        if not self.connected or not self.websocket:
            return
        
        try:
            async for message in self.websocket:
                await self._handle_message(message)
        except ConnectionClosed:
            logger.info("WebSocket connection closed")
            self.connected = False
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
            self.connected = False
    
    async def _reconnect_loop(self):
        """Reconnect to the WebSocket server if disconnected."""
        while self.running:
            if not self.connected:
                success = await self.connect()
                if success:
                    # Start receiving messages
                    asyncio.create_task(self._receive_messages())
            
            # Wait before checking connection again
            await asyncio.sleep(self.reconnect_interval)
    
    async def run(self):
        """Run the WebSocket client."""
        self.running = True
        
        # Start the reconnect loop
        reconnect_task = asyncio.create_task(self._reconnect_loop())
        
        # Wait until stopped
        while self.running:
            await asyncio.sleep(1)
        
        # Clean up
        reconnect_task.cancel()
        await self.disconnect()
    
    def stop(self):
        """Stop the WebSocket client."""
        self.running = False

# Function to start the WebSocket client in a separate thread
def start_ws_client(server_url: str, reconnect_interval: int = 5) -> threading.Thread:
    """
    Start the WebSocket client in a separate thread.
    
    Args:
        server_url: URL of the WebSocket server
        reconnect_interval: Interval in seconds to attempt reconnection
        
    Returns:
        The thread running the WebSocket client
    """
    client = WebSocketClient(server_url, reconnect_interval)
    
    # Create a new event loop for the thread
    def run_client():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(client.run())
        loop.close()
    
    # Start the client in a separate thread
    thread = threading.Thread(target=run_client, daemon=True)
    thread.start()
    
    return thread

if __name__ == "__main__":
    # Test the WebSocket client
    import time
    
    # Replace with your WebSocket server URL
    server_url = "ws://localhost:3000/ws"
    
    thread = start_ws_client(server_url)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass