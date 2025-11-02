#!/usr/bin/env python3
"""
Update version in NSIS installer script
"""
import os
import sys
import re

def update_nsis_version():
    """Update the version in the NSIS script"""
    # Get current version
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    from iso42001 import __version__
    
    # Path to NSIS script
    nsis_file = os.path.join(os.path.dirname(__file__), '..', 'build', 'iso42001-installer.nsi')
    
    # Read the file
    with open(nsis_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update version
    content = re.sub(r'!define PRODUCT_VERSION ".*"', f'!define PRODUCT_VERSION "{__version__}"', content)
    
    # Write back
    with open(nsis_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(__version__)
    return __version__

if __name__ == '__main__':
    update_nsis_version()