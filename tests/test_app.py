#!/usr/bin/env python3
"""
Test script to verify the ISO 42001 application components work correctly
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

try:
    print("Testing database module...")
    from iso42001.database import ISO42001Database
    
    # Use a test database
    db = ISO42001Database("test_iso42001.db")
    print("✓ Database module imported and initialized successfully")
    
    # Test basic database operations
    stats = db.get_dashboard_stats()
    print(f"✓ Dashboard stats retrieved: {stats}")
    
    print("\nTesting app module...")
    from iso42001 import app
    print("✓ App module imported successfully")
    
    print("\nTesting callbacks module...")
    from iso42001 import callbacks
    print("✓ Callbacks module imported successfully")
    
    print("\n✓ All modules loaded successfully!")
    print("The application should be ready to run.")
    
    # Clean up test database
    if os.path.exists("test_iso42001.db"):
        os.remove("test_iso42001.db")
        print("✓ Test database cleaned up")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()