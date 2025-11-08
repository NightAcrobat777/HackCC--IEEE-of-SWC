"""
Internship API Package
Provides Flask REST API for serving internship data
"""

from .internship_api import app
from .fetch_and_clone_internships import InternshipFetcher

__all__ = ['app', 'InternshipFetcher']
