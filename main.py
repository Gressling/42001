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
import tempfile
import atexit
import psutil

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
    
    # Create a global lock file that persists across all instances
    lock_file = os.path.join(tempfile.gettempdir(), f'iso42001_browser_global.lock')
    
    try:
        # Try to create the lock file exclusively with a timeout check
        if os.path.exists(lock_file):
            # Check if lock file is older than 10 seconds (stale lock)
            lock_age = time.time() - os.path.getmtime(lock_file)
            if lock_age > 10:
                os.remove(lock_file)
        
        with open(lock_file, 'x') as f:
            f.write(f'{os.getpid()}:{port}:{time.time()}')
        
        # Clean up lock file on exit
        def cleanup_lock():
            try:
                if os.path.exists(lock_file):
                    os.remove(lock_file)
            except:
                pass
        
        atexit.register(cleanup_lock)
        
        # Open browser
        webbrowser.open(f'http://127.0.0.1:{port}')
        
    except FileExistsError:
        # Lock file exists, browser already opened by another process
        pass

def is_first_instance():
    """Check if this is the first instance of the application"""
    current_process = psutil.Process()
    current_exe = current_process.exe()
    current_name = os.path.basename(current_exe)
    
    # Count how many processes with the same executable are running
    count = 0
    for proc in psutil.process_iter(['pid', 'exe', 'name']):
        try:
            if proc.info['exe'] == current_exe or proc.info['name'] == current_name:
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return count <= 1

if __name__ == '__main__':
    # Find a free port
    try:
        port = find_free_port()
        print("Starting ISO 42001 Bookkeeping Application...")
        print(f"Browser will open automatically at http://127.0.0.1:{port}")
        
        if port != 8050:
            print(f"Note: Using port {port} because 8050 is occupied")
        
        # Check if we should open browser - simplified approach
        should_skip_browser = os.environ.get('ISO42001_SKIP_BROWSER', '').lower() == 'true'
        
        # For executables, use a simpler lock-based approach instead of process detection
        if getattr(sys, 'frozen', False):
            # Running as executable - always try to open browser unless explicitly skipped
            should_open_browser = not should_skip_browser
        else:
            # Running as Python script - use first instance detection
            should_open_browser = not should_skip_browser and is_first_instance()
        
        if should_open_browser:
            # Start browser opening in a separate thread
            browser_thread = threading.Thread(target=open_browser, args=(port,))
            browser_thread.daemon = True
            browser_thread.start()
        
        # Check if we're running in development mode
        debug_mode = os.environ.get('ISO42001_DEBUG', 'true').lower() == 'true'
        
        # For executables, always disable reloader to prevent multiple instances
        if getattr(sys, 'frozen', False):
            debug_mode = False
            use_reloader = False
        else:
            use_reloader = debug_mode
        
        # Start the application
        app.run(debug=debug_mode, host='127.0.0.1', port=port, use_reloader=use_reloader)
        
    except RuntimeError as e:
        print(f"Error: {e}")
        print("Please close some applications and try again.")
        sys.exit(1)