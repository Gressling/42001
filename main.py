#!/usr/bin/env python3
"""
Main entry point for ISO 42001 Bookkeeping Application
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from iso42001 import app

if __name__ == '__main__':
    print("Starting ISO 42001 Bookkeeping Application...")
    print("Navigate to http://127.0.0.1:8050 to access the application")
    app.run(debug=True, host='127.0.0.1', port=8050)