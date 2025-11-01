#!/usr/bin/env python3
"""
Main entry point for ISO 42001 Bookkeeping Application
"""

import sys
import os
import webbrowser
import threading
import time
import socket

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from iso42001 import app

def find_free_port(start_port=8050, max_attempts=100):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")

def open_browser(port):
    """Open the default browser after a short delay"""
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open(f'http://127.0.0.1:{port}')

if __name__ == '__main__':
    # Find a free port
    try:
        port = find_free_port()
        print("Starting ISO 42001 Bookkeeping Application...")
        print(f"Browser will open automatically at http://127.0.0.1:{port}")
        
        if port != 8050:
            print(f"Note: Using port {port} because 8050 is occupied")
        
        # Start browser opening in a separate thread
        browser_thread = threading.Thread(target=open_browser, args=(port,))
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the application
        app.run(debug=True, host='127.0.0.1', port=port)
        
    except RuntimeError as e:
        print(f"Error: {e}")
        print("Please close some applications and try again.")
        sys.exit(1)