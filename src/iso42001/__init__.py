"""
ISO 42001 Bookkeeping Application

A Dash-based application for basic ISO 42001 AI Management System bookkeeping.
"""

__version__ = "1.1.0"
__author__ = "Gressling Consulting GmbH"
__email__ = "info@gressling.de"
__license__ = "CC BY-NC-ND 4.0"

from .app import app
from .database import ISO42001Database

__all__ = ['app', 'ISO42001Database']
