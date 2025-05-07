"""
main.py

This is the main entry point for the Raspberry Pi bedtime routine application.
It initializes and starts all components: FastAPI server, display thread, and WebSocket client.
"""

import argparse
import os
import signal
import sys
import threading
import time
from typing import Optional

# Import our modules
from fastapi_server import start_server
from display_thread import start_display_thread
from ws_client import start_ws_client
from routine_state import routine_state

# Default configuration
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_WS_URL = "ws://localhost:3000/ws"
DEFAULT_SOUND_DIR = "sounds"
DEFAULT_SCREEN_SIZE = (800, 480)
DEFAULT_FPS = 30

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Raspberry Pi Bedtime Routine Application")
    
    parser.add_argument("--host", default=DEFAULT_HOST,
                        help=f"Host to bind the FastAPI server (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help=f"Port to bind the FastAPI server (default: {DEFAULT_PORT})")
    parser.add_argument("--ws-url", default=DEFAULT_WS_URL,
                        help=f"WebSocket server URL (default: {DEFAULT_WS_URL})")
    parser.add_argument("--sound-dir", default=DEFAULT_SOUND_DIR,
                        help=f"Directory containing sound files (default: {DEFAULT_SOUND_DIR})")
    parser.add_argument("--width", type=int, default=DEFAULT_SCREEN_SIZE[0],
                        help=f"Screen width (default: {DEFAULT_SCREEN_SIZE[0]})")
    parser.add_argument("--height", type=int, default=DEFAULT_SCREEN_SIZE[1],
                        help=f"Screen height (default: {DEFAULT_SCREEN_SIZE[1]})")
    parser.add_argument("--fps", type=int, default=DEFAULT_FPS,
                        help=f"Display frames per second (default: {DEFAULT_FPS})")
    parser.add_argument("--no-display", action="store_true",
                        help="Disable pygame display (for headless operation)")
    parser.add_argument("--no-ws", action="store_true",
                        help="Disable WebSocket client")
    
    return parser.parse_args()

def main():
    """Main function to start the application."""
    # Parse command line arguments
    args = parse_args()
    
    # Create the sounds directory if it doesn't exist
    os.makedirs(args.sound_dir, exist_ok=True)
    
    # Start the display thread if enabled
    display_thread = None
    if not args.no_display:
        print(f"Starting display thread (size: {args.width}x{args.height}, fps: {args.fps})")
        display_thread = start_display_thread(
            sound_dir=args.sound_dir,
            screen_size=(args.width, args.height),
            fps=args.fps
        )
    
    # Start the WebSocket client if enabled
    ws_thread = None
    if not args.no_ws:
        print(f"Starting WebSocket client (server: {args.ws_url})")
        ws_thread = start_ws_client(server_url=args.ws_url)
    
    # Start the FastAPI server in a separate thread
    print(f"Starting FastAPI server on {args.host}:{args.port}")
    server_thread = threading.Thread(
        target=start_server,
        args=(args.host, args.port),
        daemon=True
    )
    server_thread.start()
    
    # Set up signal handling for graceful shutdown
    def signal_handler(sig, frame):
        print("Shutting down...")
        # The threads are daemon threads, so they will be terminated when the main thread exits
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())