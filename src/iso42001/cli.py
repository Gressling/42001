#!/usr/bin/env python3
"""
Command Line Interface for ISO 42001 Bookkeeping Application
"""

import argparse
import sys
import os

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="ISO 42001 AI Management System Bookkeeping Application"
    )
    
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Port to bind the server to (default: 8050)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run in debug mode"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}"
    )
    
    args = parser.parse_args()
    
    # Import and run the app
    from . import app
    
    print(f"Starting ISO 42001 Bookkeeping Application...")
    print(f"Navigate to http://{args.host}:{args.port} to access the application")
    
    app.run(debug=args.debug, host=args.host, port=args.port)

def get_version():
    """Get version from package"""
    try:
        from . import __version__
        return __version__
    except ImportError:
        return "unknown"

if __name__ == "__main__":
    main()